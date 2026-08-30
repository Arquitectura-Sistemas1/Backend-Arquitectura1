from datetime import date
from sqlalchemy.orm import Session
from app.core.database import ejecutar_sp, ejecutar_sp_commit

"""
Aquí está toda la lógica para invocar los procedimientos almacenados que son llamados
en las funciones de services/auth.py.
"""

def obtener_verificacion(db: Session, login: str, codigo: str):
    return ejecutar_sp_commit(
        db,
        "sp_ValidarCodigoRegistro",
        Login=login,
        Codigo=codigo,
        SolicitudRegistroID=None,  # OUTPUT
        EsValido=None,             # OUTPUT
        IntentosRestantes=None      # OUTPUT
    )


def obtener_validacion_registro(db: Session, solicitud_id: int):
    """
    Invoca el SP para migrar la solicitud verificada 
    a las tablas finales Usuario y CredencialUsuario
    este va junto al anterior para migrar
    """
    return ejecutar_sp_commit(
        db,
        "sp_ConfirmarRegistroUsuario",
        SolicitudRegistroID=solicitud_id,
        UsuarioID=None  # Parámetro OUTPUT de SQL Server
    )

