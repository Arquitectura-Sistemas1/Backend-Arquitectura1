from datetime import datetime
from decimal import Decimal
from typing import Literal
from pydantic import BaseModel, model_validator


# ==========================================
# 1. ASIGNAR DESCUENTO A VIDEOJUEGO
# ==========================================
class AsignarDescuentoReq(BaseModel):
    VideojuegoID: int
    DescuentoID: int = 1


class AsignarDescuentoRes(BaseModel):
    status: str
    mensaje: str
    VideojuegoID: int
    DescuentoID: int


# ==========================================
# 2. CREAR DESCUENTO
# ==========================================
class CrearDescuentoReq(BaseModel):
    Tipo: Literal["PORCENTAJE", "MONTO_FIJO"]
    Valor: Decimal
    FechaInicio: datetime
    FechaFin: datetime

    @model_validator(mode="after")
    def validar_descuento(self):
        if self.Valor < 0:
            raise ValueError("El valor del descuento debe ser mayor o igual a 0.")
        if self.Tipo == "PORCENTAJE" and self.Valor > 100:
            raise ValueError("Un descuento porcentual no puede exceder el 100%.")
        if self.FechaFin <= self.FechaInicio:
            raise ValueError("La fecha de fin debe ser posterior a la fecha de inicio.")
        return self


class CrearDescuentoRes(BaseModel):
    status: str
    mensaje: str
    DescuentoID: int
    Tipo: str
    Valor: Decimal
    FechaInicio: datetime
    FechaFin: datetime


# ==========================================
# 3. CREAR CUPÓN
# ==========================================
class CrearCuponReq(BaseModel):
    Codigo: str
    Tipo: Literal["PORCENTAJE", "MONTO_FIJO"]
    Valor: Decimal
    FechaExpiracion: datetime

    @model_validator(mode="after")
    def validar_cupon(self):
        if self.Valor < 0:
            raise ValueError("El valor del cupón debe ser mayor o igual a 0.")
        if self.Tipo == "PORCENTAJE" and self.Valor > 100:
            raise ValueError("Un cupón porcentual no puede exceder el 100%.")
        return self


class CrearCuponRes(BaseModel):
    status: str
    mensaje: str
    CuponID: int
    Codigo: str
    Tipo: str
    Valor: Decimal
    FechaExpiracion: datetime
