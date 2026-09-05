from sqlalchemy.orm import Session
from app.core.database import ejecutar_sp


def obtener_descuentos(db: Session):
    return ejecutar_sp(db, "sp_getDescuento")


def obtener_devoluciones(db: Session):
    return ejecutar_sp(db, "sp_getDevolucion")