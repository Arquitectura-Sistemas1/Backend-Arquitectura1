from sqlalchemy.orm import Session
from app.core.database import ejecutar_sp


def crear_pedido(db: Session, usuario_id: int):
    resultado = ejecutar_sp(
        db,
        "sp_CrearPedido",
        {"UsuarioID": usuario_id}
    )

    res = resultado[0]
    data = dict(res._mapping) if hasattr(res, "_mapping") else dict(res)

    return {
        "PedidoID": data.get("PedidoID")
    }