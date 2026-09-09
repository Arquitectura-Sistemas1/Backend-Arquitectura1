# ============================================
# DESTINO FINAL: app/api/endpoints/comercial.py
# ============================================
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.core.security import obtener_usuario_actual
from app.services.comercial import agregar_item_pedido
from app.schemas.comercial import AgregarItemPedidoReq, AgregarItemPedidoRes

router = APIRouter(prefix="/comercial", tags=["Comercial"])


@router.post("/agregar-item-pedido", status_code=status.HTTP_201_CREATED, response_model=AgregarItemPedidoRes)
def agregar_item_pedido_endpoint(
    datos: AgregarItemPedidoReq,
    db: Session = Depends(get_db),
    usuario_actual: str = Depends(obtener_usuario_actual),
):
    return agregar_item_pedido(db, datos)
