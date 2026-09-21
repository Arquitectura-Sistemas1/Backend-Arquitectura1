# ============================================
# DESTINO FINAL:para app/api/endpoints/item.py
# ============================================
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.services.item import obtener_generos, obtener_clasificaciones
from app.schemas.item import GeneroRes, ClasificacionRes

router = APIRouter(prefix="/item", tags=["Item"])


@router.get("/generos", status_code=status.HTTP_200_OK, response_model=list[GeneroRes])
def get_generos_endpoint(db: Session = Depends(get_db)):
    return obtener_generos(db)


@router.get("/clasificaciones", status_code=status.HTTP_200_OK, response_model=list[ClasificacionRes])
def get_clasificaciones_endpoint(db: Session = Depends(get_db)):
    return obtener_clasificaciones(db)
