from fastapi import Form
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import date, datetime


# ----------------------------------------------------
# SCHEMAS PARA CREACIÓN
# ----------------------------------------------------
class VideojuegoCreate(BaseModel):
    clasificacion_id: int
    titulo: str
    descripcion: Optional[str] = None
    fecha_lanzamiento: date
    numero_jugadores: int
    edicion: str
    idioma: str
    genero_id: int
    desarrolladora_id: int

    @classmethod
    def as_form(
        cls,
        clasificacion_id: int = Form(...),
        titulo: str = Form(...),
        descripcion: Optional[str] = Form(None),
        fecha_lanzamiento: date = Form(...),
        numero_jugadores: int = Form(...),
        edicion: str = Form(...),
        idioma: str = Form(...),
        genero_id: int = Form(...),
        desarrolladora_id: int = Form(...)
    ):
        return cls(
            clasificacion_id=clasificacion_id,
            titulo=titulo,
            descripcion=descripcion,
            fecha_lanzamiento=fecha_lanzamiento,
            numero_jugadores=numero_jugadores,
            edicion=edicion,
            idioma=idioma,
            genero_id=genero_id,
            desarrolladora_id=desarrolladora_id
        )


class VideojuegoResponse(BaseModel):
    videojuego_id: int
    portada_id: int | None = None


# ----------------------------------------------------
# SCHEMAS AUXILIARES (Estructura Anidada)
# ----------------------------------------------------
class ClasificacionSchema(BaseModel):
    id: int
    codigo: str | None = None
    edad_minima: int | None = None
    descripcion: str | None = None


class GeneroSchema(BaseModel):
    id: int
    nombre: str
    descripcion: str | None = None


class DesarrolladoraSchema(BaseModel):
    id: int
    nombre: str
    sitio_web: str | None = None


class PortadaSchema(BaseModel):
    id: int
    url: str


# ----------------------------------------------------
# SCHEMAS PARA LECTURA / CONSULTAS
# ----------------------------------------------------

# Para cuando buscas un videojuego específico
class VideojuegoGet(BaseModel):
    id: int


# Respuesta de detalle completo o catálogo anidado
class VideoGameStrictResponse(BaseModel):
    id: int
    titulo: str
    descripcion: str | None = None
    fecha_lanzamiento: date
    numero_jugadores: int
    edicion: str
    idioma: str
    fecha_creacion: datetime | None = None

    clasificacion: ClasificacionSchema | None = None
    genero: GeneroSchema | None = None
    desarrolladora: DesarrolladoraSchema | None = None
    portada: PortadaSchema | None = None

    model_config = ConfigDict(from_attributes=True)


# Si aún necesitas mantener la respuesta plana del catálogo por compatibilidad:
class VideojuegoCatalogoResponse(BaseModel):
    id: int
    titulo: str
    descripcion: str | None = None
    fecha_lanzamiento: date
    numero_jugadores: int
    edicion: str
    idioma: str
    clasificacion_id: int | None = None
    clasificacion_nombre: str | None = None
    genero_id: int | None = None
    genero_nombre: str | None = None
    desarrolladora_id: int | None = None
    desarrolladora_nombre: str | None = None
    portada_id: int | None = None
    portada_url: str | None = None