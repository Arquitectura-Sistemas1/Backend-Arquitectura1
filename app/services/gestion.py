from typing import Any
from fastapi import HTTPException, status
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.schemas.gestion import (
    SolicitarDevolucionReq,
    ActualizarEstadoDevolucionReq,
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


def solicitar_devolucion(db: Session, usuario_id: int, datos: SolicitarDevolucionReq) -> dict[str, Any]:
    """
    Registra una solicitud de devolución efectuada por el usuario autenticado para un PedidoItemID.
    """
    try:
        # 1. Verificar si el PedidoItemID pertenece al usuario autenticado
        item_row = db.execute(
            text(
                """
                SELECT pi.ID AS PedidoItemID
                FROM dbo.PedidoItem pi
                INNER JOIN dbo.Pedido p ON p.ID = pi.PedidoID
                WHERE pi.ID = :pedido_item_id AND p.UsuarioID = :usuario_id
                """
            ),
            {"pedido_item_id": datos.PedidoItemID, "usuario_id": usuario_id},
        ).mappings().first()

        if not item_row:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No se encontró el ítem de pedido {datos.PedidoItemID} asociado a tu usuario.",
            )

        # 2. Verificar si ya existe una devolución previa para este PedidoItemID
        dev_exist = db.execute(
            text("SELECT 1 FROM dbo.Devolucion WHERE PedidoItemID = :pedido_item_id"),
            {"pedido_item_id": datos.PedidoItemID},
        ).scalar()

        if dev_exist:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Ya existe una solicitud de devolución registrada para el ítem {datos.PedidoItemID}.",
            )

        # 3. Crear el registro de Devolucion en estado 'SOLICITADA'
        res = db.execute(
            text(
                """
                INSERT INTO dbo.Devolucion (PedidoItemID, UsuarioID, Motivo, Estado)
                OUTPUT INSERTED.ID AS DevolucionID
                VALUES (:pedido_item_id, :usuario_id, :motivo, 'SOLICITADA')
                """
            ),
            {
                "pedido_item_id": datos.PedidoItemID,
                "usuario_id": usuario_id,
                "motivo": datos.Motivo,
            },
        ).mappings().first()

        db.commit()
        devolucion_id = int(res["DevolucionID"])

        return {
            "status": "success",
            "mensaje": f"Solicitud de devolución {devolucion_id} creada exitosamente.",
            "DevolucionID": devolucion_id,
            "PedidoItemID": datos.PedidoItemID,
            "Estado": "SOLICITADA",
        }
    except HTTPException:
        db.rollback()
        raise
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error al solicitar devolución: {_limpiar_error_sql(e)}",
        )


def actualizar_estado_devolucion(db: Session, datos: ActualizarEstadoDevolucionReq) -> dict[str, Any]:
    """
    Actualiza el estado de una devolución (APROBADA, RECHAZADA, REEMBOLSADA) por parte de un empleado.
    """
    try:
        # 1. Verificar existencia de la devolución
        dev_row = db.execute(
            text("SELECT Estado FROM dbo.Devolucion WHERE ID = :devolucion_id"),
            {"devolucion_id": datos.DevolucionID},
        ).mappings().first()

        if not dev_row:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No se encontró la devolución con ID {datos.DevolucionID}.",
            )

        estado_actual = dev_row["Estado"]

        # Validaciones de transiciones de estado
        if estado_actual in ("RECHAZADA", "REEMBOLSADA"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"La devolución {datos.DevolucionID} ya se encuentra en estado final '{estado_actual}' y no se puede modificar.",
            )

        if datos.EstadoNuevo == "REEMBOLSADA" and estado_actual != "APROBADA":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Solo se puede cambiar a estado 'REEMBOLSADA' si la devolución se encuentra actualmente en estado 'APROBADA'.",
            )

        # 2. Actualizar estado y notas
        db.execute(
            text(
                """
                UPDATE dbo.Devolucion
                SET Estado = :estado_nuevo,
                    EmpleadoID = :empleado_id,
                    FechaResolucion = SYSDATETIME(),
                    NotasAdministrador = :notas
                WHERE ID = :devolucion_id
                """
            ),
            {
                "estado_nuevo": datos.EstadoNuevo,
                "empleado_id": datos.EmpleadoID,
                "notas": datos.NotasAdministrador,
                "devolucion_id": datos.DevolucionID,
            },
        )
        db.commit()

        return {
            "status": "success",
            "mensaje": f"Devolución {datos.DevolucionID} actualizada a estado '{datos.EstadoNuevo}'.",
            "DevolucionID": datos.DevolucionID,
            "EstadoNuevo": datos.EstadoNuevo,
            "NotasAdministrador": datos.NotasAdministrador,
        }
    except HTTPException:
        db.rollback()
        raise
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error al actualizar devolución: {_limpiar_error_sql(e)}",
        )

