# ============================================
# DESTINO FINAL: para app/schemas/item.py
# ============================================
from pydantic import BaseModel


class GeneroRes(BaseModel):
    ID: int
    Nombre: str
    Descripcion: str


class ClasificacionRes(BaseModel):
    ID: int
    Codigo: str
    EdadMinima: int
    Descripcion: str
