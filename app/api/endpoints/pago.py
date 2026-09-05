from fastapi import APIRouter, Depends, status
from app.core.database import Session
from app.api.deps import get_db
from app.services.pago import listar_metodos_pago, listar_tarifas
from app.schemas.pago import MetodoPagoRes, TarifaRes

router = APIRouter(prefix="/pago", tags=["Pago"])

@router.get("/metodos", status_code=status.HTTP_200_OK, response_model=list[MetodoPagoRes])
def listar_metodos_pago_endpoint(db: Session = Depends(get_db)):
    return listar_metodos_pago(db)

@router.get("/tarifas", status_code=status.HTTP_200_OK, response_model=list[TarifaRes])
def listar_tarifas_endpoint(db: Session = Depends(get_db)):
    return listar_tarifas(db)