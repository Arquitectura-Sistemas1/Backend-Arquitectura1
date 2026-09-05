from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.services.informacion import (
    obtener_descuentos,
    obtener_devoluciones
)
from app.schemas.informacion import (
    DescuentoRes,
    DevolucionRes
)


router = APIRouter(
    prefix="/informacion",
    tags=["Informacion"]
)


@router.get(
    "/descuentos",
    status_code=status.HTTP_200_OK,
    response_model=list[DescuentoRes]
)
def get_descuentos_endpoint(db: Session = Depends(get_db)):
    return obtener_descuentos(db)


@router.get(
    "/devoluciones",
    status_code=status.HTTP_200_OK,
    response_model=list[DevolucionRes]
)
def get_devoluciones_endpoint(db: Session = Depends(get_db)):
    return obtener_devoluciones(db)