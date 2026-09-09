from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.schemas.comercial import ProcesarPagoReq, ProcesarPagoRes
from app.services.comercial import procesar_pago


router = APIRouter(prefix="/comercial", tags=["Comercial"])


@router.post(
    "/procesar-pago",
    status_code=status.HTTP_201_CREATED,
    response_model=ProcesarPagoRes,
)
def procesar_pago_endpoint(datos: ProcesarPagoReq, db: Session = Depends(get_db)):
    return procesar_pago(db, datos)
