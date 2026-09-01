
from fastapi import APIRouter, Depends, status
from app.core.database import Session
from app.api.deps import get_db
from app.core.security import obtener_usuario_actual
from app.services.inventario import crear_videojuego, cargar_videojuegos, listar_videojuegos_catalogo
from app.schemas.inventario import (
    VideojuegoResponse,
    VideojuegoCreate,
    VideoGameStrictResponse,
    VideojuegoGet,
    VideojuegoCatalogoResponse
)
from fastapi import UploadFile, File
from fastapi import FastAPI, Depends, status, Request # <-- Importar Request
from sqlalchemy.orm import Session


router = APIRouter(prefix="/inv", tags=["Inventario"]) #uohisdhasd



@router.get("/videojuegos", status_code=status.HTTP_200_OK, response_model=list[VideojuegoCatalogoResponse])
def listar_videojuegos_catalogo_endpoint(
    request: Request, # <-- Agregar este parámetro obligatorio para slowapi
    db: Session = Depends(get_db)
):
    return listar_videojuegos_catalogo(db)

@router.post("/crear-videojuego", status_code=status.HTTP_201_CREATED, response_model=VideojuegoResponse)
def crear_videojuego_endpoint(
    datos: VideojuegoCreate = Depends(VideojuegoCreate.as_form), # <-- Inyección directa del Schema
    file: UploadFile | None = File(None),
    db: Session = Depends(get_db),
    usuario_actual: str = Depends(obtener_usuario_actual)
):
    return crear_videojuego(db, file, datos)

@router.post("/buscar-videojuego", status_code=status.HTTP_200_OK, response_model=VideoGameStrictResponse)
def buscar_videojuego_endpoint(
    datos: VideojuegoGet,
    db: Session = Depends(get_db),
    usuario_actual: str = Depends(obtener_usuario_actual)
):
    return cargar_videojuegos(db, datos)
