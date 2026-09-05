from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.schemas.info import (
    PaisResponse, PlataformaResponse, 
    RegionResponse, DesarrolladoraResponse, 
    GeneroRes, ClasificacionRes, 
    MetodoPagoRes, TarifaRes)


from app.services.info import (
    obtener_paises, obtener_plataformas, 
    obtener_regiones, obtener_desarrolladoras, 
    obtener_generos, obtener_clasificaciones, 
    listar_metodos_pago, listar_tarifas)


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

@router.get("/generos", status_code=status.HTTP_200_OK, response_model=list[GeneroRes])
def get_generos_endpoint(db: Session = Depends(get_db)):
    return obtener_generos(db)


@router.get("/clasificaciones", status_code=status.HTTP_200_OK, response_model=list[ClasificacionRes])
def get_clasificaciones_endpoint(db: Session = Depends(get_db)):
    return obtener_clasificaciones(db)


@router.get("/metodos", status_code=status.HTTP_200_OK, response_model=list[MetodoPagoRes])
def listar_metodos_pago_endpoint(db: Session = Depends(get_db)):
    return listar_metodos_pago(db)

@router.get("/tarifas", status_code=status.HTTP_200_OK, response_model=list[TarifaRes])
def listar_tarifas_endpoint(db: Session = Depends(get_db)):
    return listar_tarifas(db)
