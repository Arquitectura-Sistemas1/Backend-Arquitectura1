from sqlalchemy.orm import Session
from app.schemas.info import MetodoPagoRes, TarifaRes
from app.core.database import ejecutar_sp


def obtener_paises(db: Session):
    resultados = ejecutar_sp(db, "sp_getPais")
    return [dict(resultado) for resultado in resultados]


def obtener_plataformas(db: Session):
    resultados = ejecutar_sp(db, "sp_getPlataforma")
    return [dict(resultado) for resultado in resultados]

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


def obtener_generos(db: Session):
    return ejecutar_sp(db, "sp_getGenero")


def obtener_clasificaciones(db: Session):
    return ejecutar_sp(db, "sp_getClasificacion")


def listar_metodos_pago(db: Session) -> list[MetodoPagoRes]: #oara listar todos los metodos de pago disponibles
    resultados = ejecutar_sp(db, "sp_getMetodoPago")
    return [MetodoPagoRes(**fila) for fila in resultados]

def listar_tarifas(db: Session) -> list[TarifaRes]: #para listar todas las tarifas disponibles
    resultados = ejecutar_sp(db, "sp_getTarifa")
    return [TarifaRes(**fila) for fila in resultados]