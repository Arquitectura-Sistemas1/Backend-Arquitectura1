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


# ==========================================
# 4. CREAR TARIFA
# ==========================================
class CrearTarifaReq(BaseModel):
    PrecioVenta: Decimal | None = None
    PrecioRenta: Decimal | None = None
    DuracionRentaHoras: int | None = None

    @model_validator(mode="after")
    def validar_tarifa(self):
        if self.PrecioVenta is None and self.PrecioRenta is None:
            raise ValueError("Debe ingresar al menos un precio de venta o un precio de renta.")
        
        if self.PrecioVenta is not None and self.PrecioVenta < 0:
            raise ValueError("El precio de venta no puede ser negativo.")
            
        if self.PrecioRenta is not None:
            if self.PrecioRenta < 0:
                raise ValueError("El precio de renta no puede ser negativo.")
            if self.DuracionRentaHoras is None or self.DuracionRentaHoras <= 0:
                raise ValueError("Si ingresa un precio de renta, debe especificar una duración en horas mayor a 0.")
        else:
            if self.DuracionRentaHoras is not None:
                raise ValueError("Si no hay precio de renta, la duración de renta debe ser nula.")

        return self


class CrearTarifaRes(BaseModel):
    status: str
    mensaje: str
    TarifaID: int
    PrecioVenta: Decimal | None = None
    PrecioRenta: Decimal | None = None
    DuracionRentaHoras: int | None = None

