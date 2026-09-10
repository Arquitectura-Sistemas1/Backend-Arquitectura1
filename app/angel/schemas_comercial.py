from pydantic import BaseModel
from typing import Optional


# =====================================
# REVISAR PEDIDO
# =====================================

class RevisarPedidoReq(BaseModel):
    PedidoID: int
    EmpleadoID: int
    Aprobar: bool
    Observacion: Optional[str] = None


class RevisarPedidoRes(BaseModel):
    status: str
    mensaje: str


# =====================================
# RECALCULAR PEDIDO
# =====================================

class RecalcularPedidoReq(BaseModel):
    PedidoID: int


class RecalcularPedidoRes(BaseModel):
    status: str
    Subtotal: float
    DescuentoTotal: float
    Total: float


# =====================================
# COMPLETAR PEDIDO
# =====================================

class CompletarPedidoReq(BaseModel):
    PedidoID: int


class CompletarPedidoRes(BaseModel):
    status: str
    mensaje: str