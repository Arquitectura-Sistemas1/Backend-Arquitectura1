from sqlalchemy.orm import Session
from app.core.database import ejecutar_sp

def obtener_credencial_empleado(db: Session, login: str):

    return ejecutar_sp(db, "sp_ObtenerCredencialEmpleado", Login=login)

def obtener_credencial_usuario(db: Session, login: str):

    return ejecutar_sp(db, "sp_ObtenerCredencialUsuario", Login=login)
