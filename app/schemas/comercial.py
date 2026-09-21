from decimal import Decimal
from typing import Literal

from pydantic import BaseModel


# Dóminick Tomás: Acá definí los datos que necesito recibir para procesar el pago.
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


# Dóminick Tomás: Acá devuelvo los identificadores de la transacción y la factura.
class ProcesarPagoRes(BaseModel):
    TransaccionID: int
    FacturaID: int
