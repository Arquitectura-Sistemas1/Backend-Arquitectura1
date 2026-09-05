from pydantic import BaseModel
from typing import Optional

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

class MetodoPagoRes(BaseModel):
    ID: int
    Nombre: str
    Instrucciones: Optional[str] = None

class TarifaRes(BaseModel):
    ID: int
    PrecioVenta: float
    PrecioRenta: float
    DuracionRentaHoras: int