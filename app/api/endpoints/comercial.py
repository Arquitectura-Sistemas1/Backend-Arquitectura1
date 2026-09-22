from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.schemas.comercial import (
    ProcesarPagoReq,
    ProcesarPagoRes,
    CrearPedidoRequest,
    CrearPedidoResponse,
    AgregarItemPedidoReq,
    AgregarItemPedidoRes,
    RevisarPedidoRes,
    RecalcularPedidoRes,
    CompletarPedidoRes,
    GestionarPedidoReq,
    AplicarCuponReq,
    AplicarCuponRes,
)
from app.services.comercial import (
    gestionar_pedido,
    procesar_pago,
    crear_pedido,
    agregar_item_pedido,
    aplicar_cupon,
)
from app.core.security import obtener_usuario_actual

router = APIRouter(prefix="/comercial", tags=["Comercial"])


@router.post(
    "/procesar-pago",
    status_code=status.HTTP_201_CREATED,
    response_model=ProcesarPagoRes,
)
def procesar_pago_endpoint(
    datos: ProcesarPagoReq,
    db: Session = Depends(get_db),
    usuario_actual: str = Depends(obtener_usuario_actual),
):
    return procesar_pago(db, int(usuario_actual), datos)




@router.post(
    "/crear-pedido",
    status_code=status.HTTP_201_CREATED,
    response_model=CrearPedidoResponse
)
def crear_pedido_endpoint(
    db: Session = Depends(get_db),
    usuario_actual: str = Depends(obtener_usuario_actual),
):
    return crear_pedido(db, int(usuario_actual))




@router.post("/agregar-item-pedido", status_code=status.HTTP_201_CREATED, response_model=AgregarItemPedidoRes)
def agregar_item_pedido_endpoint(
    datos: AgregarItemPedidoReq,
    db: Session = Depends(get_db),
    usuario_actual: str = Depends(obtener_usuario_actual),
):
    return agregar_item_pedido(db, int(usuario_actual), datos)



@router.post(
    "/aplicar-cupon",
    status_code=status.HTTP_200_OK,
    response_model=AplicarCuponRes,
)
def aplicar_cupon_endpoint(
    datos: AplicarCuponReq,
    db: Session = Depends(get_db),
    usuario_actual: str = Depends(obtener_usuario_actual),
):
    """Aplica un cupón de descuento al pedido activo del usuario autenticado."""
    return aplicar_cupon(db, int(usuario_actual), datos)



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