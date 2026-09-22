from decimal import Decimal
from typing import Literal
from pydantic import BaseModel
from enum import StrEnum
from typing import Optional
from pydantic import BaseModel, model_validator
from datetime import datetime

class ProcesarPagoReq(BaseModel):
    MetodoPagoID: int
    NITCliente: str = "CF"
    NombreCliente: str



class ProcesarPagoRes(BaseModel):
    TransaccionID: int
    FacturaID: int
    NumeroFactura: str
    PDFUrl: str
    MontoTotal: Decimal




class CrearPedidoRequest(BaseModel):
    UsuarioID: int


class CrearPedidoResponse(BaseModel):
    PedidoID: int



class AgregarItemPedidoReq(BaseModel):
    VideojuegoID: int
    TipoItem: str  # 'VENTA' o 'RENTA'


class AgregarItemPedidoRes(BaseModel):
    PedidoID: int
    ProductoID: int
    PedidoItemID: int
    SKU: Optional[str] = None
    CodigoLicencia: Optional[str] = None




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


class AccionPedido(StrEnum):
    REVISAR = "REVISAR"
    RECALCULAR = "RECALCULAR"
    COMPLETAR = "COMPLETAR"


class GestionarPedidoReq(BaseModel):
    """Solicitud única para las operaciones comerciales de un pedido."""

    Accion: AccionPedido
    PedidoID: int
    EmpleadoID: Optional[int] = None
    Aprobar: Optional[bool] = None
    Observacion: Optional[str] = None

    @model_validator(mode="after")
    def validar_revision(self):
        if self.Accion == AccionPedido.REVISAR:
            if self.EmpleadoID is None:
                raise ValueError("EmpleadoID es obligatorio para la acción REVISAR.")
            if self.Aprobar is None:
                raise ValueError("Aprobar es obligatorio para la acción REVISAR.")
        return self


class RevisarPedidoRes(BaseModel):
    status: str
    mensaje: str

class RecalcularPedidoRes(BaseModel):
    status: str
    Subtotal: float
    DescuentoTotal: float
    Total: float

class CompletarPedidoRes(BaseModel):
    status: str
    mensaje: str


class AplicarCuponReq(BaseModel):
    Codigo: str


class AplicarCuponRes(BaseModel):
    status: str
    mensaje: str
    PedidoID: int
    Subtotal: float
    DescuentoTotal: float
    Total: float