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