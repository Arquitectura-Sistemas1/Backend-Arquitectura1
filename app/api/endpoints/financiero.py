from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.core.security import obtener_usuario_actual
from app.schemas.financiero import (
    AsignarDescuentoReq,
    AsignarDescuentoRes,
    CrearDescuentoReq,
    CrearDescuentoRes,
    CrearCuponReq,
    CrearCuponRes,
)
from app.services.financiero import (
    asignar_descuento,
    crear_descuento,
    crear_cupon,
)

router = APIRouter(prefix="/financiero", tags=["Financiero"])


@router.post(
    "/asignar-descuento",
    status_code=status.HTTP_200_OK,
    response_model=AsignarDescuentoRes,
)
def asignar_descuento_endpoint(
    datos: AsignarDescuentoReq,
    db: Session = Depends(get_db),
    usuario_actual: str = Depends(obtener_usuario_actual),
):
    """Asigna un descuento a un videojuego."""
    return asignar_descuento(db, datos)


@router.post(
    "/crear-descuento",
    status_code=status.HTTP_201_CREATED,
    response_model=CrearDescuentoRes,
)
def crear_descuento_endpoint(
    datos: CrearDescuentoReq,
    db: Session = Depends(get_db),
    usuario_actual: str = Depends(obtener_usuario_actual),
):
    """Crea un nuevo descuento en la base de datos."""
    return crear_descuento(db, datos)


@router.post(
    "/crear-cupon",
    status_code=status.HTTP_201_CREATED,
    response_model=CrearCuponRes,
)
def crear_cupon_endpoint(
    datos: CrearCuponReq,
    db: Session = Depends(get_db),
    usuario_actual: str = Depends(obtener_usuario_actual),
):
    """Crea un nuevo cupón promocional en la base de datos."""
    return crear_cupon(db, datos)
