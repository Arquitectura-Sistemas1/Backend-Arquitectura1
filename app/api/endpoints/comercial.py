from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.schemas.comercial import (
    ProcesarPagoReq,
    ProcesarPagoRes,
    CrearPedidoReq,
    CrearPedidoRes,
)
from app.services.comercial import procesar_pago, crear_pedido


router = APIRouter(prefix="/comercial", tags=["Comercial"])


# Dóminick Tomás: Acá implementé el endpoint que recibe la solicitud para procesar el pago.
@router.post(
    "/procesar-pago",
    status_code=status.HTTP_201_CREATED,
    response_model=ProcesarPagoRes,
)
def procesar_pago_endpoint(datos: ProcesarPagoReq, db: Session = Depends(get_db)):
    return procesar_pago(db, datos)

# Yeisson Poroj: Crea el endpoint POST para registrar un nuevo pedido mediante sp_CrearPedido.

@router.post(
    "/crear-pedido",
    status_code=status.HTTP_201_CREATED,
    response_model=CrearPedidoRes,
)
def crear_pedido_endpoint(
    datos: CrearPedidoReq,
    db: Session = Depends(get_db)
):
    return crear_pedido(db, datos)