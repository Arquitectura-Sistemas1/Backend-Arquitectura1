from datetime import date
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.core.database import ejecutar_sp, ejecutar_sp_commit

from app.crud.auth import (
    obtener_solicitud_registro,
    obtener_verificacion,
    obtener_validacion_registro
)
from app.core.security import hasher, comparar_hash
from app.externalservices.msjresend import enviar_correo
from app.schemas.auth import LoginReq, LoginRes, UsuarioInfo, SolicitudUsuarioReq
from app.utils.codesgen import generar_codigo_verificacion
"""aca recordar que crud.auth.py solo es la funcion que manda a llamar los procedimientos almacenados
services los convierte en logica de creacion en db y negocio
endpoints solo llaman a las funciones que hacen toda esta logica
vamos a usar schemas para no andar referenciando el gran cuerpo de datos a cada rato
"""



def login_usuario(datos: LoginReq, db: Session):
    try:
        # 1 Buscar en la tabla de usuarios
        resultados_usuario = ejecutar_sp(db, "sp_ObtenerCredencialUsuario", Login=datos.usuario)
        
        if resultados_usuario:
            credencial = resultados_usuario[0]
            if not comparar_hash(datos.psswd, credencial['HashContrasena']):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED, 
                    detail="Contraseña incorrecta."
                )
            return {
                "message": "Inicio de sesión exitoso",
        "access_token": "123",
        "token_type": "bearer",
        "usuario": {
            "usuario_id": credencial["UsuarioID"], # o UsuarioID
            "usuario": credencial["Usuario"],
            "correo": credencial["Correo"],
            "tipo_cuenta": "Usuario"
                }
            }

        # 2 Si no existe como usuario, buscar en la tabla de empleados
        resultados_empleado = ejecutar_sp(db, "sp_ObtenerCredencialEmpleado", Login=datos.usuario)
        
        if resultados_empleado:
            credencial = resultados_empleado[0]
            if not comparar_hash(datos.psswd, credencial['HashContrasena']):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED, 
                    detail="Contraseña incorrecta."
                )
            return {
                "message": "Inicio de sesión exitoso",
                        "access_token": "123",
                        "token_type": "bearer",
                        "usuario": {
                            "usuario_id": credencial["UsuarioID"], # o UsuarioID
                            "usuario": credencial["Usuario"],
                            "correo": credencial["Correo"],
                            "tipo_cuenta": "Empleado"
                }
            }

        # 3 Si no existe en ninguno
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Usuario o correo no encontrado en el sistema."
        )

    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error BD en consulta de credenciales: {str(e.__dict__.get('orig', e))}"
        )




def solicitud_usuario(db: Session, datos: SolicitudUsuarioReq, minutos_validez: int = 10, max_intentos: int = 5,):
    try:
 
        hash_password = hasher(datos.password)
        codigo = generar_codigo_verificacion()
        resultado = ejecutar_sp_commit(
        db,
        "sp_CrearSolicitudRegistro",
        Nombres=datos.nombres,
        Apellidos=datos.apellidos,
        FechaNacimiento=datos.fecha_nacimiento,
        Telefono=datos.telefono,
        Correo=datos.correo,
        PaisID=datos.pais_id,
        Usuario=datos.usuario,
        HashContrasena=hash_password,
        Codigo=codigo,
        MinutosValidez=minutos_validez,
        MaxIntentos=max_intentos,
        SolicitudRegistroID=None,  # Parametro OUTPUT en SQL Server
        CodigoRegistroID=None,     # Parametro OUTPUT en SQL Server
    )

        # 3 Validar resultado de BD ANTES de enviar correo
        if not resultado:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No se pudo crear la solicitud de registro."
            )

        # 4 Enviar correo solo si la inserción en BD fue exitosa
        try:
            enviar_correo(datos.nombres, datos.correo, codigo, "registro")
        except Exception as mail_err:
            print(f"[WARNING] No se pudo enviar el correo a {datos.correo}: {str(mail_err)}")
        res = resultado[0] if isinstance(resultado, list) else resultado
        return {
            "message": "Solicitud de registro creada exitosamente.",
            "data": {
                "solicitud_registro_id": res["SolicitudRegistroID"],
                "codigo_registro_id": res["CodigoRegistroID"]}
        }

    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error BD al crear solicitud: {str(e.__dict__.get('orig', e))}"
        )




def registrar_usuario_final(solicitud_id: int, db: Session):
    try:
        resultado = obtener_validacion_registro(db, solicitud_id=solicitud_id)
        if not resultado:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No se pudo completar el registro. Verifica que la solicitud esté VERIFICADA."
            )
        return {
            "message": "Usuario registrado exitosamente en el sistema.",
            "data": resultado[0] if isinstance(resultado, list) else resultado
        }
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error BD al completar registro: {str(e.__dict__.get('orig', e))}"
        )
#el de arriba es para meter el reguisro y el de abajo para migrar el usuario a la db
def verificar_registro (usuario: str, code: str, db: Session):
    try:
        resultados = obtener_verificacion(db, login=usuario, codigo=code)
        if not resultados:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario o correo no encontrado"
            )
        return resultados[0]
    except SQLAlchemyError as e:
        raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error BD: {str(e.__dict__.get('orig', e))}"
                )