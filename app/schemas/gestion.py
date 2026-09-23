from typing import Optional, Literal
from pydantic import BaseModel


class SolicitarDevolucionReq(BaseModel):
    PedidoItemID: int
    Motivo: str


class SolicitarDevolucionRes(BaseModel):
    status: str
    mensaje: str
    DevolucionID: int
    PedidoItemID: int
    Estado: str


class ActualizarEstadoDevolucionReq(BaseModel):
    DevolucionID: int
    EmpleadoID: int
    EstadoNuevo: Literal["APROBADA", "RECHAZADA", "REEMBOLSADA"]
    NotasAdministrador: Optional[str] = None


class ActualizarEstadoDevolucionRes(BaseModel):
    status: str
    mensaje: str
    DevolucionID: int
    EstadoNuevo: str
    NotasAdministrador: Optional[str] = None

