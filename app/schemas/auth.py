from pydantic import BaseModel, EmailStr

class LoginReq(BaseModel):
    usuario: str
    psswd: str

class UsuarioInfo(BaseModel):
    usuario_id: int
    usuario: str
    correo: EmailStr
    tipo_cuenta: str

class LoginRes(BaseModel):
    message: str = "Inicio de Sesion Exitoso"
    access_token = str
    token_type: str = "bearer"
    usuario : UsuarioInfo