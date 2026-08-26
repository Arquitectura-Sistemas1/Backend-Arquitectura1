from sqlalchemy.orm import Session
from app.core.database import ejecutar_sp
"""aqui esta toda la logica para invocar los procedimientos almacenados que son llamados
en lasfunciones de services/auth.py y en general todas las funciones de servicios
los servicios se diferencian como las funciones que ejecutan los procedimientos
"""

def obtener_credencial_empleado(db: Session, login: str):

    return ejecutar_sp(db, "sp_ObtenerCredencialEmpleado", Login=login)

def obtener_credencial_usuario(db: Session, login: str):

    return ejecutar_sp(db, "sp_ObtenerCredencialUsuario", Login=login)
