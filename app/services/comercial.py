from typing import Any, Optional
from decimal import Decimal
from datetime import datetime


from fastapi import HTTPException, status
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.core.database import ejecutar_sp_commit
from app.schemas.comercial import (
    ProcesarPagoReq,
    AgregarItemPedidoReq,
    AccionPedido,
    GestionarPedidoReq,
    AplicarCuponReq,
)

from app.utils import (
    generar_referencia_externa,
    generar_numero_factura,
    generar_imagen_factura,
    generar_sku,
    generar_codigo_licencia,
)

from app.externalservices.nubecloudi import subir_factura_imagen






def _limpiar_error_sql(e: Exception) -> str:
    """Extrae el mensaje en español lanzado por THROW en SQL Server sin formato técnico de pymssql."""
    orig = getattr(e, "orig", e)
    if hasattr(orig, "args") and len(orig.args) > 1:
        raw_msg = orig.args[1]
        if isinstance(raw_msg, bytes):
            return raw_msg.decode("utf-8", errors="ignore").split("DB-Lib")[0].strip()
        if isinstance(raw_msg, str):
            return raw_msg.split("DB-Lib")[0].strip()
    return str(orig)


def _ejecutar_sp_out(
    db: Session,
    nombre_sp: str,
    out_param: str,
    params: dict[str, Any]
) -> int:
    """Ejecuta un Stored Procedure que declara un parámetro OUTPUT y retorna su valor entero."""
    param_assignments = ", ".join(f"@{k} = :{k}" for k in params.keys())
    separator = ", " if param_assignments else ""
    sql = text(
        f"""
        DECLARE @{out_param} BIGINT;
        EXEC dbo.{nombre_sp} {param_assignments}{separator}@{out_param} = @{out_param} OUTPUT;
        SELECT @{out_param} AS {out_param};
        """
    )
    resultado = db.execute(sql, params)
    fila = resultado.mappings().first()
    if not fila or fila.get(out_param) is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"El Stored Procedure '{nombre_sp}' no devolvió {out_param}.",
        )
    return int(fila[out_param])


def crear_pedido(db: Session, usuario_id: int) -> dict[str, int]:
    """1. Crea un pedido inicial para un usuario mediante sp_CrearPedido."""
    try:
        pedido_id = _ejecutar_sp_out(
            db,
            "sp_CrearPedido",
            "PedidoID",
            {"UsuarioID": usuario_id},
        )
        db.commit()
        return {"PedidoID": pedido_id}
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error al crear pedido: {_limpiar_error_sql(e)}",
        )


def agregar_item_pedido(db: Session, usuario_id: int, datos: AgregarItemPedidoReq) -> dict[str, Any]:
    """2. Crea un nuevo Producto (con SKU y Licencia únicos) para el VideojuegoID especificado y lo agrega al pedido activo."""
    try:
        # 0. Remover el constraint UNIQUE 'UQ_Producto_Videojuego' si existe en la BD
        try:
            db.execute(text("ALTER TABLE dbo.Producto DROP CONSTRAINT UQ_Producto_Videojuego"))
            db.commit()
        except Exception:
            db.rollback()

        # 1. Consultar información del videojuego para generar SKU y Licencia
        v_row = db.execute(
            text(
                """
                SELECT 
                    v.Titulo,
                    COALESCE(pl.Nombre, 'GEN') AS PlataformaNombre,
                    COALESCE(r.Nombre, 'GLOBAL') AS RegionNombre
                FROM dbo.Videojuego v
                LEFT JOIN dbo.Plataforma pl ON pl.ID = v.PlataformaID
                LEFT JOIN dbo.Region r ON r.ID = v.RegionID
                WHERE v.ID = :videojuego_id
                """
            ),
            {"videojuego_id": datos.VideojuegoID},
        ).mappings().first()

        if not v_row:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No se encontró el videojuego con ID {datos.VideojuegoID}.",
            )

        titulo = v_row["Titulo"]
        plataforma = v_row["PlataformaNombre"]
        region = v_row["RegionNombre"]

        # 2. Calcular número de secuencia global de productos para el Código de Licencia (PROD-KEY-001, PROD-KEY-002...)
        total_prods = db.execute(text("SELECT COUNT(*) FROM dbo.Producto")).scalar() or 0
        codigo_licencia = generar_codigo_licencia(secuencia=total_prods + 1)

        # 3. Calcular cantidad de productos de este videojuego para el SKU
        prods_videojuego = db.execute(
            text("SELECT COUNT(*) FROM dbo.Producto WHERE VideojuegoID = :videojuego_id"),
            {"videojuego_id": datos.VideojuegoID},
        ).scalar() or 0

        sku = generar_sku(titulo, plataforma, region, secuencia=prods_videojuego + 1)

        # 4. Insertar nuevo registro siempre en dbo.Producto
        prod_row = db.execute(
            text(
                """
                INSERT INTO dbo.Producto (VideojuegoID, SKU, Codigo_Licencia)
                OUTPUT INSERTED.ProductoID
                VALUES (:videojuego_id, :sku, :codigo_licencia)
                """
            ),
            {
                "videojuego_id": datos.VideojuegoID,
                "sku": sku,
                "codigo_licencia": codigo_licencia,
            },
        ).mappings().first()

        if not prod_row or not prod_row.get("ProductoID"):
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="No se pudo registrar la copia de producto para este videojuego.",
            )

        producto_id = int(prod_row["ProductoID"])



        # 4. Buscar el pedido activo (CREADO o PENDIENTE_PAGO) más reciente del usuario
        pedido_row = db.execute(
            text(
                """
                SELECT TOP 1 ID AS PedidoID
                FROM dbo.Pedido
                WHERE UsuarioID = :usuario_id
                  AND Estado IN ('CREADO', 'PENDIENTE_PAGO')
                ORDER BY FechaCreacion DESC
                """
            ),
            {"usuario_id": usuario_id},
        ).mappings().first()

        if pedido_row and pedido_row.get("PedidoID"):
            pedido_id = int(pedido_row["PedidoID"])
        else:
            res_crear = crear_pedido(db, usuario_id)
            pedido_id = res_crear["PedidoID"]

        # 5. Agregar el Producto recién creado al pedido mediante el Stored Procedure
        pedido_item_id = _ejecutar_sp_out(
            db,
            "sp_AgregarItemPedido",
            "PedidoItemID",
            {
                "PedidoID": pedido_id,
                "ProductoID": producto_id,
                "TipoItem": datos.TipoItem,
            },
        )
        db.commit()
        return {
            "PedidoID": pedido_id,
            "ProductoID": producto_id,
            "PedidoItemID": pedido_item_id,
            "SKU": sku,
            "CodigoLicencia": codigo_licencia,
        }
    except HTTPException:
        db.rollback()
        raise
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error al agregar ítem al pedido: {_limpiar_error_sql(e)}",
        )










def procesar_pago(db: Session, usuario_id: int, datos: ProcesarPagoReq) -> dict[str, Any]:
    """
    Registra el pago y genera la factura calculando el monto desde la BD,
    buscando el pedido activo en estado PENDIENTE_PAGO del usuario autenticado.
    """
    try:
        # 1. Obtener los totales del pedido y los datos del cupón del pedido activo del usuario
        pedido_row = db.execute(
            text(
                """
                SELECT TOP 1
                    p.ID AS PedidoID,
                    p.Subtotal, 
                    p.DescuentoTotal, 
                    p.Total,
                    c.Codigo AS CuponCodigo,
                    c.Tipo AS CuponTipo,
                    c.Valor AS CuponValor
                FROM dbo.Pedido p
                LEFT JOIN dbo.Cupon c ON c.ID = p.CuponID
                WHERE p.UsuarioID = :usuario_id AND p.Estado = 'PENDIENTE_PAGO'
                ORDER BY p.FechaCreacion DESC
                """
            ),
            {"usuario_id": usuario_id},
        ).mappings().first()

        if not pedido_row or pedido_row.get("Total") is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No tienes ningún pedido en estado PENDIENTE_PAGO para procesar.",
            )

        pedido_id = int(pedido_row["PedidoID"])
        subtotal = float(pedido_row.get("Subtotal", 0) or 0)
        descuento_total = float(pedido_row.get("DescuentoTotal", 0) or 0)
        monto_total = Decimal(str(pedido_row["Total"]))

        # 2. Obtener los ítems asociados al pedido
        items_rows = db.execute(
            text(
                """
                SELECT 
                    COALESCE(v.Titulo, 'Producto') AS Videojuego,
                    pi.TipoItem,
                    pi.PrecioAplicado AS Precio,
                    pi.DescuentoAplicado AS Descuento,
                    (pi.PrecioAplicado - pi.DescuentoAplicado) AS Subtotal
                FROM dbo.PedidoItem pi
                INNER JOIN dbo.Producto pr ON pr.ProductoID = pi.ProductoID
                INNER JOIN dbo.Videojuego v ON v.ID = pr.VideojuegoID
                WHERE pi.PedidoID = :pedido_id
                """
            ),
            {"pedido_id": pedido_id},
        ).mappings().all()

        items_list = [dict(row) for row in items_rows]

        # 3. Generar referencia externa, número de factura y fecha
        referencia_externa = generar_referencia_externa()
        numero_factura = generar_numero_factura()
        fecha_actual = datetime.now().strftime("%d/%m/%Y %H:%M")
        estado_pago = "APROBADA"

        # 4. Generar la imagen PNG de la factura en memoria (incluyendo datos de cupón si existen)
        datos_factura = {
            "numero_factura": numero_factura,
            "referencia_externa": referencia_externa,
            "fecha": fecha_actual,
            "nombre_cliente": datos.NombreCliente,
            "nit_cliente": datos.NITCliente,
            "items": items_list,
            "subtotal": subtotal,
            "descuento_total": descuento_total,
            "total": float(monto_total),
            "cupon_codigo": pedido_row.get("CuponCodigo"),
            "cupon_tipo": pedido_row.get("CuponTipo"),
            "cupon_valor": pedido_row.get("CuponValor"),
        }
        png_bytes = generar_imagen_factura(datos_factura)

        # 5. Subir imagen PNG a Cloudinary exactamente igual que subir_imagen
        pdf_url = subir_factura_imagen(numero_factura, png_bytes)

        # 6. Registrar el pago en la BD (actualiza el pedido a 'PAGADO')
        transaccion_id = _ejecutar_sp_out(
            db,
            "sp_RegistrarPago",
            "TransaccionID",
            {
                "PedidoID": pedido_id,
                "MetodoPagoID": datos.MetodoPagoID,
                "Monto": monto_total,
                "ReferenciaExterna": referencia_externa,
                "Estado": estado_pago,
            },
        )


        # 7. Generar la factura en la BD
        factura_id = _ejecutar_sp_out(
            db,
            "sp_GenerarFactura",
            "FacturaID",
            {
                "TransaccionID": transaccion_id,
                "NumeroFactura": numero_factura,
                "NITCliente": datos.NITCliente,
                "NombreCliente": datos.NombreCliente,
                "PDFUrl": pdf_url,
            },
        )

        db.commit()

        return {
            "TransaccionID": transaccion_id,
            "FacturaID": factura_id,
            "NumeroFactura": numero_factura,
            "PDFUrl": pdf_url,
            "MontoTotal": monto_total,
        }
    except HTTPException:
        db.rollback()
        raise
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error al procesar pago: {_limpiar_error_sql(e)}",
        )




def gestionar_pedido(db: Session, datos: GestionarPedidoReq) -> dict[str, Any]:
    """4. Acciones administrativas / gestión comercial sobre el pedido (REVISAR, RECALCULAR, COMPLETAR)."""
    try:
        if datos.Accion == AccionPedido.REVISAR:
            ejecutar_sp_commit(
                db,
                "sp_RevisarPedido",
                PedidoID=datos.PedidoID,
                EmpleadoID=datos.EmpleadoID,
                Aprobar=datos.Aprobar,
                Observacion=datos.Observacion,
            )
            res_str = "APROBADO" if datos.Aprobar else "RECHAZADO"
            return {
                "status": "success",
                "mensaje": f"Pedido {datos.PedidoID} revisado y cambiado a estado {res_str}.",
            }

        if datos.Accion == AccionPedido.RECALCULAR:
            ejecutar_sp_commit(
                db,
                "sp_RecalcularPedido",
                PedidoID=datos.PedidoID,
            )
            res = db.execute(
                text("SELECT Subtotal, DescuentoTotal, Total FROM dbo.Pedido WHERE ID = :id"),
                {"id": datos.PedidoID},
            ).mappings().first()
            return {
                "status": "success",
                "Subtotal": float(res["Subtotal"]) if res and res["Subtotal"] is not None else 0.0,
                "DescuentoTotal": float(res["DescuentoTotal"]) if res and res["DescuentoTotal"] is not None else 0.0,
                "Total": float(res["Total"]) if res and res["Total"] is not None else 0.0,
            }

        # AccionPedido.COMPLETAR
        ejecutar_sp_commit(
            db,
            "sp_CompletarPedido",
            PedidoID=datos.PedidoID,
        )
        return {
            "status": "success",
            "mensaje": f"Pedido {datos.PedidoID} completado exitosamente.",
        }
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=_limpiar_error_sql(e),
        )


def aplicar_cupon(db: Session, usuario_id: int, datos: AplicarCuponReq) -> dict[str, Any]:
    """Aplica un cupón de descuento al pedido activo del usuario autenticado mediante sp_AplicarCupon."""
    try:
        # Buscar el pedido activo (CREADO o PENDIENTE_PAGO) más reciente del usuario
        pedido_row = db.execute(
            text(
                """
                SELECT TOP 1 ID AS PedidoID
                FROM dbo.Pedido
                WHERE UsuarioID = :usuario_id
                  AND Estado IN ('CREADO', 'PENDIENTE_PAGO')
                ORDER BY FechaCreacion DESC
                """
            ),
            {"usuario_id": usuario_id},
        ).mappings().first()

        if not pedido_row or not pedido_row.get("PedidoID"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No tienes ningún pedido activo en estado CREADO o PENDIENTE_PAGO para aplicar un cupón.",
            )

        pedido_id = int(pedido_row["PedidoID"])

        # Ejecutar el SP que valida el cupón y recalcula los totales
        ejecutar_sp_commit(
            db,
            "sp_AplicarCupon",
            PedidoID=pedido_id,
            Codigo=datos.Codigo,
        )

        # Consultar los nuevos totales del pedido
        totales_row = db.execute(
            text("SELECT Subtotal, DescuentoTotal, Total FROM dbo.Pedido WHERE ID = :pedido_id"),
            {"pedido_id": pedido_id},
        ).mappings().first()

        return {
            "status": "success",
            "mensaje": f"Cupón '{datos.Codigo}' aplicado exitosamente al pedido {pedido_id}.",
            "PedidoID": pedido_id,
            "Subtotal": float(totales_row["Subtotal"]) if totales_row and totales_row["Subtotal"] is not None else 0.0,
            "DescuentoTotal": float(totales_row["DescuentoTotal"]) if totales_row and totales_row["DescuentoTotal"] is not None else 0.0,
            "Total": float(totales_row["Total"]) if totales_row and totales_row["Total"] is not None else 0.0,
        }
    except HTTPException:
        db.rollback()
        raise
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=_limpiar_error_sql(e),
        )