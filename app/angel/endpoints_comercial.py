from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.deps import get_db

from app.services.comercial import (
    revisar_pedido,
    recalcular_pedido,
    completar_pedido
)

from app.schemas.comercial import (
    RevisarPedidoReq,
    RevisarPedidoRes,
    RecalcularPedidoReq,
    RecalcularPedidoRes,
    CompletarPedidoReq,
    CompletarPedidoRes
)

router = APIRouter(
    prefix="/comercial",
    tags=["Comercial"]
)

# =====================================
# REVISAR PEDIDO
# =====================================

@router.put(
    "/revisar-pedido",
    status_code=status.HTTP_200_OK,
    response_model=RevisarPedidoRes
)
def revisar_pedido_endpoint(
    datos: RevisarPedidoReq,
    db: Session = Depends(get_db)
):
    return revisar_pedido(
        db,
        datos.PedidoID,
        datos.EmpleadoID,
        datos.Aprobar,
        datos.Observacion
    )


# =====================================
# RECALCULAR PEDIDO
# =====================================

@router.post(
    "/recalcular-pedido",
    status_code=status.HTTP_200_OK,
    response_model=RecalcularPedidoRes
)
def recalcular_pedido_endpoint(
    datos: RecalcularPedidoReq,
    db: Session = Depends(get_db)
):
    return recalcular_pedido(
        db,
        datos.PedidoID
    )


# =====================================
# COMPLETAR PEDIDO
# =====================================

@router.post(
    "/completar-pedido",
    status_code=status.HTTP_200_OK,
    response_model=CompletarPedidoRes
)
def completar_pedido_endpoint(
    datos: CompletarPedidoReq,
    db: Session = Depends(get_db)
):
    return completar_pedido(
        db,
        datos.PedidoID
    )