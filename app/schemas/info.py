from pydantic import BaseModel


class PaisResponse(BaseModel):
    ID: int
    Nombre: str


class PlataformaResponse(BaseModel):
    ID: int
    Nombre: str
    Fabricante: str

class RegionResponse(BaseModel):
    id: int
    nombre: str


class DesarrolladoraResponse(BaseModel):
    id: int
    nombre: str
    sitio_web: str | None = None

class GeneroRes(BaseModel):
    ID: int
    Nombre: str
    Descripcion: str


class ClasificacionRes(BaseModel):
    ID: int
    Codigo: str
    EdadMinima: int
    Descripcion: str