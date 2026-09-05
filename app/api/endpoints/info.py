from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.schemas.info import PaisResponse, PlataformaResponse, RegionResponse, DesarrolladoraResponse
from app.services.info import obtener_paises, obtener_plataformas, obtener_regiones, obtener_desarrolladoras


router = APIRouter(prefix="/info", tags=["informacion"])


@router.get("/paises", status_code=status.HTTP_200_OK, response_model=list[PaisResponse])
def obtener_paises_endpoint(db: Session = Depends(get_db)):
    return obtener_paises(db)


@router.get(
    "/plataformas",
    status_code=status.HTTP_200_OK,
    response_model=list[PlataformaResponse],
)
def obtener_plataformas_endpoint(db: Session = Depends(get_db)):
    return obtener_plataformas(db)

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