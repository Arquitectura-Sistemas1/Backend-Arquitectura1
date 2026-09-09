# ============================================
# DESTINO FINAL: app/services/comercial.py
# ============================================
from sqlalchemy.orm import Session
from app.core.database import ejecutar_sp_commit
from app.schemas.comercial import AgregarItemPedidoReq


def agregar_item_pedido(db: Session, datos: AgregarItemPedidoReq):
    resultado = ejecutar_sp_commit(
        db,
        "sp_AgregarItemPedido",
        PedidoID=datos.PedidoID,
        ProductoID=datos.ProductoID,
        TipoItem=datos.TipoItem,
    )
    res = resultado[0]
    return {"PedidoItemID": res["PedidoItemID"]}
