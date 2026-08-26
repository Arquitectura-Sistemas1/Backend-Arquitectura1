from datetime import date
from sqlalchemy.orm import Session
from app.core.database import ejecutar_sp, ejecutar_sp_commit

"""
Aquí está toda la lógica para invocar los procedimientos almacenados que son llamados
en las funciones de services/auth.py.
"""
#nada mas para forzar push pidaiopsjd
def obtener_credencial_empleado(db: Session, login: str):
    return ejecutar_sp(db, "sp_ObtenerCredencialEmpleado", Login=login)

def obtener_credencial_usuario(db: Session, login: str):
    return ejecutar_sp(db, "sp_ObtenerCredencialUsuario", Login=login)
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
def completar_registro_usuario(db: Session, solicitud_id: int):
    """
    Invoca el SP para migrar la solicitud verificada 
    a las tablas finales Usuario y CredencialUsuario.
    """
    return ejecutar_sp_commit(
        db,
        "sp_ConfirmarRegistroUsuario",
        SolicitudRegistroID=solicitud_id,
        UsuarioID=None  # Parámetro OUTPUT de SQL Server
    )

def solicitar_registro(
    db: Session,
    nombres: str,
    apellidos: str,
    fecha_nacimiento: date,
    correo: str,
    pais_id: int,
    usuario: str,
    hash_contrasena: str,
    codigo: str,
    telefono: str | None = None,
    minutos_validez: int = 10,
    max_intentos: int = 5,
):
    return ejecutar_sp_commit(
        db,
        "sp_CrearSolicitudRegistro",
        Nombres=nombres,
        Apellidos=apellidos,
        FechaNacimiento=fecha_nacimiento,
        Telefono=telefono,
        Correo=correo,
        PaisID=pais_id,
        Usuario=usuario,
        HashContrasena=hash_contrasena,
        Codigo=codigo,
        MinutosValidez=minutos_validez,
        MaxIntentos=max_intentos,
        SolicitudRegistroID=None,  # Parametro OUTPUT en SQL Server
        CodigoRegistroID=None,     # Parametro OUTPUT en SQL Server
    )