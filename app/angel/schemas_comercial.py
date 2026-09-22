from enum import StrEnum
from typing import Optional

from pydantic import BaseModel, model_validator


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
