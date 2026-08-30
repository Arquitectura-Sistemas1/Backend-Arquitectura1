
from fastapi import APIRouter, Depends, status
from app.core.database import Session
from app.api.deps import get_db
from app.services.inventario import crear_videojuego
from app.schemas.inventario import VideojuegoResponse, VideojuegoCreate
from fastapi import UploadFile, File

router = APIRouter(prefix="/inv", tags=["Inventario"]) #uohisdhasd

@router.post("/crear-videojuego", status_code=status.HTTP_201_CREATED, response_model=VideojuegoResponse)
def crear_videojuego_endpoint(
    datos: VideojuegoCreate = Depends(VideojuegoCreate.as_form), # <-- Inyección directa del Schema
    file: UploadFile | None = File(None),
    db: Session = Depends(get_db)
):
    return crear_videojuego(db=db, file=file, datos=datos)