# ============================================
# DESTINO FINAL: app/schemas/comercial.py
# ============================================
from pydantic import BaseModel


class AgregarItemPedidoReq(BaseModel):
    PedidoID: int
    ProductoID: int
    TipoItem: str  # 'VENTA' o 'RENTA'


class AgregarItemPedidoRes(BaseModel):
    PedidoItemID: int
