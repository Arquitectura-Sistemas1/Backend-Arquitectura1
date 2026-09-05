from pydantic import BaseModel
from typing import Optional
from datetime import datetime
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

class DescuentoRes(BaseModel):
    ID: int
    ProductoID: int
    Tipo: str
    Valor: float
    FechaInicio: datetime
    FechaFin: datetime


class DevolucionRes(BaseModel):
    ID: int
    PedidoItemID: int
    UsuarioID: int
    EmpleadoID: Optional[int] = None
    FechaSolicitud: datetime
    Motivo: str
    Estado: str
    FechaResolucion: Optional[datetime] = None
    NotasAdministrador: Optional[str] = None