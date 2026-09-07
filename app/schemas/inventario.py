from datetime import date, datetime
from decimal import Decimal
from typing import Optional
from fastapi import Form
from pydantic import BaseModel, ConfigDict


# ====================================================
# 1. SCHEMAS PARA CREACIÓN Y REGISTRO
# ====================================================

class VideojuegoCreate(BaseModel):
    plataforma_id: int
    clasificacion_id: int
    region_id: int
    tarifa_id: int
    descuento_id: int
    titulo: str
    descripcion: str
    fecha_lanzamiento: date
    num_jugadores: int = 1
    edicion: str
    genero_id: Optional[int] = None
    desarrolladora_id: Optional[int] = None

    @classmethod
    def as_form(
        cls,
        plataforma_id: int = Form(...),
        clasificacion_id: int = Form(...),
        region_id: int = Form(...),
        tarifa_id: int = Form(...),
        descuento_id: int = Form(...),
        titulo: str = Form(...),
        descripcion: str = Form(...),
        fecha_lanzamiento: date = Form(...),
        num_jugadores: int = Form(1),
        edicion: str = Form(...),
        genero_id: Optional[int] = Form(None),
        desarrolladora_id: Optional[int] = Form(None),
    ):
        return cls(
            plataforma_id=plataforma_id,
            clasificacion_id=clasificacion_id,
            region_id=region_id,
            tarifa_id=tarifa_id,
            descuento_id=descuento_id,
            titulo=titulo,
            descripcion=descripcion,
            fecha_lanzamiento=fecha_lanzamiento,
            num_jugadores=num_jugadores,
            edicion=edicion,
            genero_id=genero_id,
            desarrolladora_id=desarrolladora_id,
        )


class VideojuegoResponse(BaseModel):
    videojuego_id: int
    portada_id: Optional[int] = None


# ====================================================
# 2. SCHEMAS AUXILIARES (Estructuras Anidadas)
# ====================================================

class PlataformaSchema(BaseModel):
    id: int
    nombre: Optional[str] = None


class RegionSchema(BaseModel):
    id: int
    nombre: Optional[str] = None


class TarifaSchema(BaseModel):
    id: int
    precio_venta: Optional[Decimal] = None
    precio_renta: Optional[Decimal] = None
    duracion_renta_horas: Optional[int] = None


class DescuentoSchema(BaseModel):
    id: int
    tipo: Optional[str] = None
    valor: Optional[Decimal] = None
    fecha_inicio: Optional[datetime] = None
    fecha_fin: Optional[datetime] = None


class ClasificacionSchema(BaseModel):
    id: int
    codigo: Optional[str] = None
    edad_minima: Optional[int] = None
    descripcion: Optional[str] = None


class GeneroSchema(BaseModel):
    id: int
    nombre: Optional[str] = None
    descripcion: Optional[str] = None


class DesarrolladoraSchema(BaseModel):
    id: int
    nombre: Optional[str] = None
    sitio_web: Optional[str] = None


class PortadaSchema(BaseModel):
    id: int
    url: str


# ====================================================
# 3. SCHEMAS PARA LECTURA Y BÚSQUEDA
# ====================================================

# Schema de solicitud para buscar por ID
class VideojuegoGet(BaseModel):
    id: int


# Respuesta para el detalle anidado estricto (Usado en /buscar-videojuego)
class VideoGameStrictResponse(BaseModel):
    id: int
    titulo: str
    descripcion: Optional[str] = None
    fecha_lanzamiento: date
    num_jugadores: int
    edicion: str
    fecha_creacion: Optional[datetime] = None

    plataforma: Optional[PlataformaSchema] = None
    region: Optional[RegionSchema] = None
    tarifa: Optional[TarifaSchema] = None
    descuento: Optional[DescuentoSchema] = None

    clasificacion: Optional[ClasificacionSchema] = None
    genero: Optional[GeneroSchema] = None
    desarrolladora: Optional[DesarrolladoraSchema] = None
    portada: Optional[PortadaSchema] = None

    model_config = ConfigDict(from_attributes=True)


# Respuesta plana para listados/catálogo masivo
class VideojuegoCatalogoResponse(BaseModel):
    id: int
    titulo: str
    descripcion: Optional[str] = None
    fecha_lanzamiento: date
    num_jugadores: int
    edicion: str

    # Plataforma y Región
    plataforma_id: Optional[int] = None
    plataforma_nombre: Optional[str] = None
    region_id: Optional[int] = None
    region_nombre: Optional[str] = None

    # Tarifa y Descuento
    tarifa_id: Optional[int] = None
    precio_venta: Optional[Decimal] = None
    precio_renta: Optional[Decimal] = None
    duracion_renta_horas: Optional[int] = None

    descuento_id: Optional[int] = None
    descuento_tipo: Optional[str] = None
    descuento_valor: Optional[Decimal] = None
    descuento_fecha_inicio: Optional[datetime] = None
    descuento_fecha_fin: Optional[datetime] = None

    # Clasificación, Género, Desarrolladora, Portada
    clasificacion_id: Optional[int] = None
    clasificacion_nombre: Optional[str] = None
    genero_id: Optional[int] = None
    genero_nombre: Optional[str] = None
    desarrolladora_id: Optional[int] = None
    desarrolladora_nombre: Optional[str] = None
    portada_id: Optional[int] = None
    portada_url: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)