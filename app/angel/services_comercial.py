from sqlalchemy.orm import Session
from app.core.database import ejecutar_sp


# =====================================
# REVISAR PEDIDO
# =====================================

def revisar_pedido(
    db: Session,
    pedido_id: int,
    empleado_id: int,
    aprobar: bool,
    observacion: str | None = None
):
    parametros = {
        "PedidoID": pedido_id,
        "EmpleadoID": empleado_id,
        "Aprobar": aprobar,
        "Observacion": observacion
    }

    return ejecutar_sp(
        db,
        "sp_RevisarPedido",
        parametros
    )


# =====================================
# RECALCULAR PEDIDO
# =====================================

def recalcular_pedido(
    db: Session,
    pedido_id: int
):
    parametros = {
        "PedidoID": pedido_id
    }

    return ejecutar_sp(
        db,
        "sp_RecalcularPedido",
        parametros
    )


# =====================================
# COMPLETAR PEDIDO
# =====================================

def completar_pedido(
    db: Session,
    pedido_id: int
):
    parametros = {
        "PedidoID": pedido_id
    }

    return ejecutar_sp(
        db,
        "sp_CompletarPedido",
        parametros
    )