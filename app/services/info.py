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