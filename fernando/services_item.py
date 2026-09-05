# ============================================
# DESTINO FINAL: para app/services/item.py
# ============================================
from sqlalchemy.orm import Session
from app.core.database import ejecutar_sp


def obtener_generos(db: Session):
    return ejecutar_sp(db, "sp_getGenero")


def obtener_clasificaciones(db: Session):
    return ejecutar_sp(db, "sp_getClasificacion")
