from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.core.security import obtener_usuario_actual
from app.schemas.gestion import (
    SolicitarDevolucionReq,
    SolicitarDevolucionRes,
    ActualizarEstadoDevolucionReq,
    ActualizarEstadoDevolucionRes,
)
from app.services.gestion import (
    solicitar_devolucion,
    actualizar_estado_devolucion,
)

router = APIRouter(prefix="/gestion", tags=["Gestion"])


@router.post(
    "/solicitar-devolucion",
    status_code=status.HTTP_201_CREATED,
    response_model=SolicitarDevolucionRes,
)
def solicitar_devolucion_endpoint(
    datos: SolicitarDevolucionReq,
    db: Session = Depends(get_db),
    usuario_actual: str = Depends(obtener_usuario_actual),
):
    """Permite a un cliente registrar una solicitud de devolución para un ítem comprado/rentado."""
    return solicitar_devolucion(db, int(usuario_actual), datos)


@router.post(
    "/actualizar-estado-devolucion",
    status_code=status.HTTP_200_OK,
    response_model=ActualizarEstadoDevolucionRes,
)
def actualizar_estado_devolucion_endpoint(
    datos: ActualizarEstadoDevolucionReq,
    db: Session = Depends(get_db),
):
    """Permite a un empleado actualizar el estado de una devolución (APROBADA, RECHAZADA, REEMBOLSADA)."""
    return actualizar_estado_devolucion(db, datos)

