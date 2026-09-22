from typing import Any
from fastapi import HTTPException, status
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.schemas.financiero import (
    AsignarDescuentoReq,
    CrearDescuentoReq,
    CrearCuponReq,
)


def _limpiar_error_sql(e: Exception) -> str:
    """Extrae el mensaje en español lanzado por SQL Server sin formato técnico de pymssql."""
    orig = getattr(e, "orig", e)
    if hasattr(orig, "args") and len(orig.args) > 1:
        raw_msg = orig.args[1]
        if isinstance(raw_msg, bytes):
            return raw_msg.decode("utf-8", errors="ignore").split("DB-Lib")[0].strip()
        if isinstance(raw_msg, str):
            return raw_msg.split("DB-Lib")[0].strip()
    return str(orig)


def asignar_descuento(db: Session, datos: AsignarDescuentoReq) -> dict[str, Any]:
    """
    Asigna un DescuentoID a un VideojuegoID en dbo.Videojuego.
    Garantiza que DescuentoID nunca sea nulo (por defecto 1 = Sin Descuento).
    """
    try:
        descuento_id = datos.DescuentoID if datos.DescuentoID is not None else 1

        # 1. Verificar si el videojuego existe
        v_exists = db.execute(
            text("SELECT 1 FROM dbo.Videojuego WHERE ID = :videojuego_id"),
            {"videojuego_id": datos.VideojuegoID},
        ).scalar()

        if not v_exists:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No se encontró el videojuego con ID {datos.VideojuegoID}.",
            )

        # 2. Verificar que el DescuentoID exista en dbo.Descuento
        d_exists = db.execute(
            text("SELECT 1 FROM dbo.Descuento WHERE ID = :descuento_id"),
            {"descuento_id": descuento_id},
        ).scalar()

        if not d_exists:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No se encontró el descuento con ID {descuento_id}.",
            )

        # 3. Actualizar la columna DescuentoID en dbo.Videojuego
        db.execute(
            text(
                """
                UPDATE dbo.Videojuego
                SET DescuentoID = :descuento_id
                WHERE ID = :videojuego_id
                """
            ),
            {
                "descuento_id": descuento_id,
                "videojuego_id": datos.VideojuegoID,
            },
        )
        db.commit()

        return {
            "status": "success",
            "mensaje": f"Descuento {descuento_id} asignado exitosamente al videojuego {datos.VideojuegoID}.",
            "VideojuegoID": datos.VideojuegoID,
            "DescuentoID": descuento_id,
        }
    except HTTPException:
        db.rollback()
        raise
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error al asignar descuento: {_limpiar_error_sql(e)}",
        )


def crear_descuento(db: Session, datos: CrearDescuentoReq) -> dict[str, Any]:
    """Crea un nuevo descuento en dbo.Descuento."""
    try:
        res = db.execute(
            text(
                """
                INSERT INTO dbo.Descuento (Tipo, Valor, FechaInicio, FechaFin)
                OUTPUT INSERTED.ID AS DescuentoID
                VALUES (:tipo, :valor, :fecha_inicio, :fecha_fin)
                """
            ),
            {
                "tipo": datos.Tipo,
                "valor": datos.Valor,
                "fecha_inicio": datos.FechaInicio,
                "fecha_fin": datos.FechaFin,
            },
        ).mappings().first()

        db.commit()
        descuento_id = int(res["DescuentoID"])

        return {
            "status": "success",
            "mensaje": f"Descuento {descuento_id} creado exitosamente.",
            "DescuentoID": descuento_id,
            "Tipo": datos.Tipo,
            "Valor": datos.Valor,
            "FechaInicio": datos.FechaInicio,
            "FechaFin": datos.FechaFin,
        }
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error al crear descuento: {_limpiar_error_sql(e)}",
        )


def crear_cupon(db: Session, datos: CrearCuponReq) -> dict[str, Any]:
    """Crea un nuevo cupón promocional en dbo.Cupon."""
    try:
        cupon_exist = db.execute(
            text("SELECT 1 FROM dbo.Cupon WHERE Codigo = :codigo"),
            {"codigo": datos.Codigo},
        ).scalar()

        if cupon_exist:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Ya existe un cupón registrado con el código '{datos.Codigo}'.",
            )

        res = db.execute(
            text(
                """
                INSERT INTO dbo.Cupon (Codigo, Tipo, Valor, FechaExpiracion)
                OUTPUT INSERTED.ID AS CuponID
                VALUES (:codigo, :tipo, :valor, :fecha_expiracion)
                """
            ),
            {
                "codigo": datos.Codigo,
                "tipo": datos.Tipo,
                "valor": datos.Valor,
                "fecha_expiracion": datos.FechaExpiracion,
            },
        ).mappings().first()

        db.commit()
        cupon_id = int(res["CuponID"])

        return {
            "status": "success",
            "mensaje": f"Cupón '{datos.Codigo}' creado exitosamente.",
            "CuponID": cupon_id,
            "Codigo": datos.Codigo,
            "Tipo": datos.Tipo,
            "Valor": datos.Valor,
            "FechaExpiracion": datos.FechaExpiracion,
        }
    except HTTPException:
        db.rollback()
        raise
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error al crear cupón: {_limpiar_error_sql(e)}",
        )
