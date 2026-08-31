from fastapi import Form
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import date


#estos son para crear los videojuegos
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

#sta cosa opara definir form que permita ingreso de file
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

#este la respuesta que da el sp de crear videojuego
class VideojuegoResponse(BaseModel):
    videojuego_id: int
    portada_id: int | None = None


#a partir de aca los schemas auziliares y el proncipal de la respuesta del sp para obtener data videojuego
class ClasificacionSchema(BaseModel):
    id: int
    codigo: str
    edad_minima: int
    descripcion: str


class GeneroSchema(BaseModel):
    id: int
    nombre: str
    descripcion: str


class DesarrolladoraSchema(BaseModel):
    id: int
    nombre: str
    sitio_web: str


class PortadaSchema(BaseModel):
    id: int
    url: str


class VideoGameStrictResponse(BaseModel):
    id: int
    titulo: str
    descripcion: str
    fecha_lanzamiento: date
    numero_jugadores: int
    edicion: str
    idioma: str

    clasificacion: ClasificacionSchema
    genero: GeneroSchema
    desarrolladora: DesarrolladoraSchema
    portada: PortadaSchema

    model_config = ConfigDict(from_attributes=True)

#este para el ingreso, es chiquito y solo de 1 parametro pero se usa para darle a todo un schema y que permita json en ingreso
class VideojuegoGet(BaseModel):
    id : int


