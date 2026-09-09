from pydantic import BaseModel


class CrearPedidoRequest(BaseModel):
    UsuarioID: int


class CrearPedidoResponse(BaseModel):
    PedidoID: int