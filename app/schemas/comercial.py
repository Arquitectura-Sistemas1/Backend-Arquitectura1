from decimal import Decimal
from typing import Literal

from pydantic import BaseModel


class ProcesarPagoReq(BaseModel):
    PedidoID: int
    MetodoPagoID: int
    Monto: Decimal
    ReferenciaExterna: str
    Estado: Literal["PENDIENTE", "APROBADA", "RECHAZADA"]
    NumeroFactura: str
    NITCliente: str
    NombreCliente: str
    PDFUrl: str


class ProcesarPagoRes(BaseModel):
    TransaccionID: int
    FacturaID: int
