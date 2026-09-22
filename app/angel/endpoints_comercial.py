from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.deps import get_db

from app.schemas.comercial import (
    RevisarPedidoRes,
    RecalcularPedidoRes,
    CompletarPedidoRes,
    GestionarPedidoReq,
)
from app.services.comercial import gestionar_pedido

router = APIRouter(
    prefix="/comercial",
    tags=["Comercial"]
)

@router.post(
    "/gestionar-pedido",
    status_code=status.HTTP_200_OK,
    response_model=RevisarPedidoRes | RecalcularPedidoRes | CompletarPedidoRes,
)
def gestionar_pedido_endpoint(
    datos: GestionarPedidoReq,
    db: Session = Depends(get_db),
):
    """Un único endpoint para revisar, recalcular o completar un pedido."""
    return gestionar_pedido(db, datos)
