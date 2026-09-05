from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.services.informacion import (
    obtener_regiones,
    obtener_desarrolladoras
)
from app.schemas.informacion import (
    RegionResponse,
    DesarrolladoraResponse
)


router = APIRouter(
    prefix="/info",
    tags=["Informacion"]
)


@router.get(
    "/regiones",
    status_code=status.HTTP_200_OK,
    response_model=list[RegionResponse]
)
def obtener_regiones_endpoint(
    db: Session = Depends(get_db)
):
    return obtener_regiones(db)


@router.get(
    "/desarrolladoras",
    status_code=status.HTTP_200_OK,
    response_model=list[DesarrolladoraResponse]
)
def obtener_desarrolladoras_endpoint(
    db: Session = Depends(get_db)
):
    return obtener_desarrolladoras(db)