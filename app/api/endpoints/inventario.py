
from fastapi import APIRouter, Depends, status
from app.core.database import Session
from app.api.deps import get_db
from app.services.inventario import crear_videojuego
from app.schemas.inventario import VideojuegoResponse, VideojuegoCreate

router = APIRouter(prefix="/inv", tags=["Inventario"]) #uohisdhasd

@router.post("/crear-videojuego", status_code=status.HTTP_201_CREATED, response_model=VideojuegoResponse)
def crear_videojuego_endpoint (payload: VideojuegoCreate, db: Session = Depends(get_db)):
    return crear_videojuego(db=db, datos=payload)
