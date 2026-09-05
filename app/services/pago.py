from sqlalchemy.orm import Session
from schemas.pago import MetodoPagoRes, TarifaRes
from core.database import ejecutar_sp  #ajusta el import según donde este definida

def listar_metodos_pago(db: Session) -> list[MetodoPagoRes]: #oara listar todos los metodos de pago disponibles
    resultados = ejecutar_sp(db, "sp_getMetodoPago")
    return [MetodoPagoRes(**fila) for fila in resultados]

def listar_tarifas(db: Session) -> list[TarifaRes]: #para listar todas las tarifas disponibles
    resultados = ejecutar_sp(db, "sp_getTarifa")
    return [TarifaRes(**fila) for fila in resultados]