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


class PedidoItemRes(BaseModel):
    PedidoItemID: int
    PedidoID: int
    ProductoID: int
    TipoItem: str
    PrecioAplicado: float
    DescuentoAplicado: float
    Subtotal: float
    VideojuegoID: int
    VideojuegoTitulo: str
    SKU: Optional[str] = None
    CodigoLicencia: Optional[str] = None
    PortadaURL: Optional[str] = None


class PedidoActualRes(BaseModel):
    PedidoID: Optional[int] = None
    Subtotal: float = 0.0
    DescuentoTotal: float = 0.0
    Total: float = 0.0
    Items: list[PedidoItemRes] = []


class PedidoResumenRes(BaseModel):
    PedidoID: int
    Estado: str
    Subtotal: float
    DescuentoTotal: float
    Impuestos: float
    Total: float
    FechaCreacion: datetime
    NumeroFactura: Optional[str] = None
    FacturaURL: Optional[str] = None


class DetallePedidoRes(BaseModel):
    PedidoID: int
    Estado: str
    Subtotal: float
    DescuentoTotal: float
    Impuestos: float
    Total: float
    FechaCreacion: datetime
    NumeroFactura: Optional[str] = None
    FacturaURL: Optional[str] = None
    Items: list[PedidoItemRes] = []


class MiDevolucionRes(BaseModel):
    DevolucionID: int
    PedidoItemID: int
    FechaSolicitud: datetime
    Motivo: str
    Estado: str
    FechaResolucion: Optional[datetime] = None
    NotasAdministrador: Optional[str] = None
    VideojuegoTitulo: str
    TipoItem: str
    PrecioAplicado: float