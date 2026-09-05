from pydantic import BaseModel
from datetime import datetime
from typing import Optional


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