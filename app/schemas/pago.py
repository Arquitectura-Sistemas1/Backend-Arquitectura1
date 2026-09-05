from pydantic import BaseModel
from typing import Optional

#nombres declarados igual q en los procesos almacenados 

class MetodoPagoRes(BaseModel):
    ID: int
    Nombre: str
    Instrucciones: Optional[str] = None

class TarifaRes(BaseModel):
    ID: int
    PrecioVenta: float
    PrecioRenta: float
    DuracionRentaHoras: int