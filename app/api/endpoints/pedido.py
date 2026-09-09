from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.services.pedido import crear_pedido
from app.schemas.pedido import CrearPedidoRequest, CrearPedidoResponse


router = APIRouter(
    prefix="/pedidos",
    tags=["Pedidos"]
)


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=CrearPedidoResponse
)
def crear_pedido_endpoint(
    pedido: CrearPedidoRequest,
    db: Session = Depends(get_db)
):
    return crear_pedido(db, pedido.UsuarioID)