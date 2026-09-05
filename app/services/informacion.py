from sqlalchemy.orm import Session

from app.core.database import ejecutar_sp


def obtener_paises(db: Session):
    resultados = ejecutar_sp(db, "sp_getPais")
    return [dict(resultado) for resultado in resultados]


def obtener_plataformas(db: Session):
    resultados = ejecutar_sp(db, "sp_getPlataforma")
    return [dict(resultado) for resultado in resultados]
