
from typing import Any
from sqlalchemy import text
from sqlalchemy.orm import Session

def ejecutar_sp(db: Session, nombre_procedimiento: str, **parametros: Any):

    lista_parametros = ", ".join(f"@{key} = :{key}" for key in parametros)
    sql = text(f"EXEC dbo.{nombre_procedimiento} {lista_parametros}")
    resultado = db.execute(sql, parametros)
    return resultado.mappings().all()

def obtener_credencial_empleado(db: Session, login: str):

    return ejecutar_sp(db, "sp_ObtenerCredencialEmpleado", Login=login)

def obtener_credencial_usuario(db: Session, login: str):

    return ejecutar_sp(db, "sp_ObtenerCredencialUsuario", Login=login)
