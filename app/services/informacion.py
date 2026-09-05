from sqlalchemy.orm import Session
from app.core.database import ejecutar_sp


def obtener_regiones(db: Session):
    resultado = ejecutar_sp(db, "sp_getRegion")

    lista = []

    for res in resultado:
        data = dict(res._mapping) if hasattr(res, "_mapping") else dict(res)

        lista.append({
            "id": data.get("ID"),
            "nombre": data.get("Nombre")
        })

    return lista


def obtener_desarrolladoras(db: Session):
    resultado = ejecutar_sp(db, "sp_getDesarrolladora")

    lista = []

    for res in resultado:
        data = dict(res._mapping) if hasattr(res, "_mapping") else dict(res)

        lista.append({
            "id": data.get("ID"),
            "nombre": data.get("Nombre"),
            "sitio_web": data.get("SitioWeb")
        })

    return lista