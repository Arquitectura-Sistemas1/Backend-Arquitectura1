from typing import Any

from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.core.database import ejecutar_sp_commit
from app.schemas.comercial import ProcesarPagoReq


def _obtener_primera_fila(resultado: Any) -> dict[str, Any]:
    if not resultado:
        return {}

    primera_fila = resultado[0]
    return dict(primera_fila._mapping) if hasattr(primera_fila, "_mapping") else dict(primera_fila)


def registrar_pago(db: Session, datos: ProcesarPagoReq) -> int:
    try:
        resultado = ejecutar_sp_commit(
            db,
            "sp_RegistrarPago",
            PedidoID=datos.PedidoID,
            MetodoPagoID=datos.MetodoPagoID,
            Monto=datos.Monto,
            ReferenciaExterna=datos.ReferenciaExterna,
            Estado=datos.Estado,
        )
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error BD al registrar pago: {str(e.__dict__.get('orig', e))}",
        )

    fila = _obtener_primera_fila(resultado)
    transaccion_id = fila.get("TransaccionID")

    if transaccion_id is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="El Stored Procedure 'sp_RegistrarPago' no devolvió TransaccionID.",
        )

    return int(transaccion_id)


def generar_factura(db: Session, transaccion_id: int, datos: ProcesarPagoReq) -> int:
    try:
        resultado = ejecutar_sp_commit(
            db,
            "sp_GenerarFactura",
            TransaccionID=transaccion_id,
            NumeroFactura=datos.NumeroFactura,
            NITCliente=datos.NITCliente,
            NombreCliente=datos.NombreCliente,
            PDFUrl=datos.PDFUrl,
        )
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error BD al generar factura: {str(e.__dict__.get('orig', e))}",
        )

    fila = _obtener_primera_fila(resultado)
    factura_id = fila.get("FacturaID")

    if factura_id is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="El Stored Procedure 'sp_GenerarFactura' no devolvió FacturaID.",
        )

    return int(factura_id)


def procesar_pago(db: Session, datos: ProcesarPagoReq) -> dict[str, int]:
    transaccion_id = registrar_pago(db, datos)
    factura_id = generar_factura(db, transaccion_id, datos)

    return {
        "TransaccionID": transaccion_id,
        "FacturaID": factura_id,
    }
