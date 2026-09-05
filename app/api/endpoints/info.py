from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.schemas.info import PaisResponse, PlataformaResponse
from app.services.info import obtener_paises, obtener_plataformas


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