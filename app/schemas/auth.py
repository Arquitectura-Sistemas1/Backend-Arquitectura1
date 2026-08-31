from pydantic import BaseModel, EmailStr
from datetime import date

class LoginReq(BaseModel):
    usuario: str
    psswd: str

class UsuarioInfo(BaseModel):
    usuario_id: int
    usuario: str
    tipo_cuenta: str

class LoginRes(BaseModel):
    message: str = "Inicio de Sesion Exitoso"
    usuario : UsuarioInfo

class SolicitudUsuarioReq(BaseModel):
    nombres: str
    apellidos: str
    fecha_nacimiento: date
    correo: EmailStr
    pais_id: int
    usuario: str
    password: str
    telefono: str | None = None

class SolicitudUsuarioData(BaseModel):
    solicitud_registro_id: int
    codigo_registro_id: int
    
class SolicitudUsuarioRes(BaseModel):
    message: str = "Solicitud de registro creada exitosamente."
    data: SolicitudUsuarioData

class ConfirmaRegistroReq(BaseModel):
    usuario: str
    codigo: str

class ConfirmaRegistroData(BaseModel):
    usuario_id: int
    solicitud_registro_id: int

class ConfirmaRegistroRes(BaseModel):
    message: str
    data: ConfirmaRegistroData