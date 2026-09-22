from sqlalchemy.orm import Session
from app.core.database import ejecutar_sp
from app.schemas.comercial import AccionPedido, GestionarPedidoReq


def gestionar_pedido(db: Session, datos: GestionarPedidoReq):
    """Ejecuta el SP comercial que corresponde a la acción solicitada."""
    if datos.Accion == AccionPedido.REVISAR:
        return ejecutar_sp(
            db,
            "sp_RevisarPedido",
            {
                "PedidoID": datos.PedidoID,
                "EmpleadoID": datos.EmpleadoID,
                "Aprobar": datos.Aprobar,
                "Observacion": datos.Observacion,
            },
        )

    if datos.Accion == AccionPedido.RECALCULAR:
        return ejecutar_sp(
            db,
            "sp_RecalcularPedido",
            {"PedidoID": datos.PedidoID},
        )

    return ejecutar_sp(
        db,
        "sp_CompletarPedido",
        {"PedidoID": datos.PedidoID},
    )
