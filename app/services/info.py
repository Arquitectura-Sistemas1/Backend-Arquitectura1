from sqlalchemy.orm import Session
from app.schemas.info import MetodoPagoRes, TarifaRes
from app.core.database import ejecutar_sp


def obtener_paises(db: Session):
    resultados = ejecutar_sp(db, "sp_getPais")
    return [dict(resultado) for resultado in resultados]


def obtener_plataformas(db: Session):
    resultados = ejecutar_sp(db, "sp_getPlataforma")
    return [dict(resultado) for resultado in resultados]

def obtener_regiones(db: Session):
    resultado = ejecutar_sp(db, "sp_getRegion")

    lista = []

    for res in resultado:
        data = dict(res._mapping) if hasattr(res, "_mapping") else dict(res)

        lista.append({
            "id": data.get("ID"),
            "nombre": data.get("Nombre")
        })

    return lista


def obtener_desarrolladoras(db: Session):
    resultado = ejecutar_sp(db, "sp_getDesarrolladora")

    lista = []

    for res in resultado:
        data = dict(res._mapping) if hasattr(res, "_mapping") else dict(res)

        lista.append({
            "id": data.get("ID"),
            "nombre": data.get("Nombre"),
            "sitio_web": data.get("SitioWeb")
        })

    return lista


def obtener_generos(db: Session):
    return ejecutar_sp(db, "sp_getGenero")


def obtener_clasificaciones(db: Session):
    return ejecutar_sp(db, "sp_getClasificacion")


def listar_metodos_pago(db: Session) -> list[MetodoPagoRes]: #oara listar todos los metodos de pago disponibles
    resultados = ejecutar_sp(db, "sp_getMetodoPago")
    return [MetodoPagoRes(**fila) for fila in resultados]

def listar_tarifas(db: Session) -> list[TarifaRes]: #para listar todas las tarifas disponibles
    resultados = ejecutar_sp(db, "sp_getTarifa")
    return [TarifaRes(**fila) for fila in resultados]


def obtener_descuentos(db: Session):
    return ejecutar_sp(db, "sp_getDescuento")


def obtener_devoluciones(db: Session):
    return ejecutar_sp(db, "sp_getDevolucion")


def obtener_pedido_actual_items(db: Session, usuario_id: int):
    """
    Obtiene los detalles y los ítems del pedido activo (CREADO o PENDIENTE_PAGO) del usuario autenticado.
    """
    from sqlalchemy import text

    # 1. Buscar el pedido activo
    pedido_row = db.execute(
        text(
            """
            SELECT TOP 1 ID, Subtotal, DescuentoTotal, Total
            FROM dbo.Pedido
            WHERE UsuarioID = :usuario_id
              AND Estado IN ('CREADO', 'PENDIENTE_PAGO')
            ORDER BY FechaCreacion DESC
            """
        ),
        {"usuario_id": usuario_id},
    ).mappings().first()

    if not pedido_row or not pedido_row.get("ID"):
        return {
            "PedidoID": None,
            "Subtotal": 0.0,
            "DescuentoTotal": 0.0,
            "Total": 0.0,
            "Items": []
        }

    pedido_id = int(pedido_row["ID"])

    # 2. Consultar los ítems asociados al pedido
    items_rows = db.execute(
        text(
            """
            SELECT 
                pi.ID AS PedidoItemID,
                pi.PedidoID,
                pi.ProductoID,
                pi.TipoItem,
                CAST(pi.PrecioAplicado AS FLOAT) AS PrecioAplicado,
                CAST(pi.DescuentoAplicado AS FLOAT) AS DescuentoAplicado,
                CAST((pi.PrecioAplicado - pi.DescuentoAplicado) AS FLOAT) AS Subtotal,
                v.ID AS VideojuegoID,
                v.Titulo AS VideojuegoTitulo,
                pr.SKU,
                pr.Codigo_Licencia AS CodigoLicencia,
                (
                    SELECT TOP 1 URL 
                    FROM dbo.Portada 
                    WHERE VideojuegoID = v.ID 
                    ORDER BY ID ASC
                ) AS PortadaURL
            FROM dbo.PedidoItem pi
            INNER JOIN dbo.Producto pr ON pr.ProductoID = pi.ProductoID
            INNER JOIN dbo.Videojuego v ON v.ID = pr.VideojuegoID
            WHERE pi.PedidoID = :pedido_id
            ORDER BY pi.ID ASC
            """
        ),
        {"pedido_id": pedido_id},
    ).mappings().all()

    items = [dict(row) for row in items_rows]

    return {
        "PedidoID": pedido_id,
        "Subtotal": float(pedido_row.get("Subtotal") or 0.0),
        "DescuentoTotal": float(pedido_row.get("DescuentoTotal") or 0.0),
        "Total": float(pedido_row.get("Total") or 0.0),
        "Items": items
    }


def obtener_mis_pedidos(db: Session, usuario_id: int):
    """
    Obtiene la lista de todos los pedidos realizados por el usuario autenticado con su estado y factura si aplica.
    """
    from sqlalchemy import text

    rows = db.execute(
        text(
            """
            SELECT 
                p.ID AS PedidoID,
                p.Estado,
                CAST(p.Subtotal AS FLOAT) AS Subtotal,
                CAST(p.DescuentoTotal AS FLOAT) AS DescuentoTotal,
                CAST(p.Impuestos AS FLOAT) AS Impuestos,
                CAST(p.Total AS FLOAT) AS Total,
                p.FechaCreacion,
                (
                    SELECT TOP 1 f.PDFUrl
                    FROM dbo.Transaccion t
                    INNER JOIN dbo.Factura f ON f.TransaccionID = t.ID
                    WHERE t.PedidoID = p.ID
                    ORDER BY f.FechaEmision DESC
                ) AS FacturaURL,
                (
                    SELECT TOP 1 f.NumeroFactura
                    FROM dbo.Transaccion t
                    INNER JOIN dbo.Factura f ON f.TransaccionID = t.ID
                    WHERE t.PedidoID = p.ID
                    ORDER BY f.FechaEmision DESC
                ) AS NumeroFactura
            FROM dbo.Pedido p
            WHERE p.UsuarioID = :usuario_id
            ORDER BY p.FechaCreacion DESC
            """
        ),
        {"usuario_id": usuario_id},
    ).mappings().all()

    return [dict(r) for r in rows]


def obtener_detalle_pedido(db: Session, usuario_id: int, pedido_id: int):
    """
    Obtiene el detalle completo de un pedido específico por ID (encabezado, factura e ítems),
    validando que pertenezca al usuario autenticado.
    """
    from sqlalchemy import text
    from fastapi import HTTPException, status

    pedido_row = db.execute(
        text(
            """
            SELECT 
                p.ID AS PedidoID,
                p.Estado,
                CAST(p.Subtotal AS FLOAT) AS Subtotal,
                CAST(p.DescuentoTotal AS FLOAT) AS DescuentoTotal,
                CAST(p.Impuestos AS FLOAT) AS Impuestos,
                CAST(p.Total AS FLOAT) AS Total,
                p.FechaCreacion,
                (
                    SELECT TOP 1 f.PDFUrl
                    FROM dbo.Transaccion t
                    INNER JOIN dbo.Factura f ON f.TransaccionID = t.ID
                    WHERE t.PedidoID = p.ID
                    ORDER BY f.FechaEmision DESC
                ) AS FacturaURL,
                (
                    SELECT TOP 1 f.NumeroFactura
                    FROM dbo.Transaccion t
                    INNER JOIN dbo.Factura f ON f.TransaccionID = t.ID
                    WHERE t.PedidoID = p.ID
                    ORDER BY f.FechaEmision DESC
                ) AS NumeroFactura
            FROM dbo.Pedido p
            WHERE p.ID = :pedido_id AND p.UsuarioID = :usuario_id
            """
        ),
        {"pedido_id": pedido_id, "usuario_id": usuario_id},
    ).mappings().first()

    if not pedido_row:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se encontró el pedido con ID {pedido_id}.",
        )

    items_rows = db.execute(
        text(
            """
            SELECT 
                pi.ID AS PedidoItemID,
                pi.PedidoID,
                pi.ProductoID,
                pi.TipoItem,
                CAST(pi.PrecioAplicado AS FLOAT) AS PrecioAplicado,
                CAST(pi.DescuentoAplicado AS FLOAT) AS DescuentoAplicado,
                CAST((pi.PrecioAplicado - pi.DescuentoAplicado) AS FLOAT) AS Subtotal,
                v.ID AS VideojuegoID,
                v.Titulo AS VideojuegoTitulo,
                pr.SKU,
                pr.Codigo_Licencia AS CodigoLicencia,
                (
                    SELECT TOP 1 URL 
                    FROM dbo.Portada 
                    WHERE VideojuegoID = v.ID 
                    ORDER BY ID ASC
                ) AS PortadaURL
            FROM dbo.PedidoItem pi
            INNER JOIN dbo.Producto pr ON pr.ProductoID = pi.ProductoID
            INNER JOIN dbo.Videojuego v ON v.ID = pr.VideojuegoID
            WHERE pi.PedidoID = :pedido_id
            ORDER BY pi.ID ASC
            """
        ),
        {"pedido_id": pedido_id},
    ).mappings().all()

    items = [dict(row) for row in items_rows]

    return {
        "PedidoID": int(pedido_row["PedidoID"]),
        "Estado": pedido_row["Estado"],
        "Subtotal": float(pedido_row["Subtotal"] or 0.0),
        "DescuentoTotal": float(pedido_row["DescuentoTotal"] or 0.0),
        "Impuestos": float(pedido_row["Impuestos"] or 0.0),
        "Total": float(pedido_row["Total"] or 0.0),
        "FechaCreacion": pedido_row["FechaCreacion"],
        "NumeroFactura": pedido_row.get("NumeroFactura"),
        "FacturaURL": pedido_row.get("FacturaURL"),
        "Items": items,
    }


def obtener_mis_devoluciones(db: Session, usuario_id: int):
    """
    Obtiene el historial de solicitudes de devolución del usuario autenticado.
    """
    from sqlalchemy import text

    rows = db.execute(
        text(
            """
            SELECT 
                d.ID AS DevolucionID,
                d.PedidoItemID,
                d.FechaSolicitud,
                d.Motivo,
                d.Estado,
                d.FechaResolucion,
                d.NotasAdministrador,
                v.Titulo AS VideojuegoTitulo,
                pi.TipoItem,
                CAST(pi.PrecioAplicado AS FLOAT) AS PrecioAplicado
            FROM dbo.Devolucion d
            INNER JOIN dbo.PedidoItem pi ON pi.ID = d.PedidoItemID
            INNER JOIN dbo.Producto pr ON pr.ProductoID = pi.ProductoID
            INNER JOIN dbo.Videojuego v ON v.ID = pr.VideojuegoID
            WHERE d.UsuarioID = :usuario_id
            ORDER BY d.FechaSolicitud DESC
            """
        ),
        {"usuario_id": usuario_id},
    ).mappings().all()

    return [dict(r) for r in rows]