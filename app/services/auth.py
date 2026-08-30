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
from app.schemas.auth import LoginReq, LoginRes, UsuarioInfo

"""aca recordar que crud.auth.py solo es la funcion que manda a llamar los procedimientos almacenados
services los convierte en logica de creacion en db y negocio
endpoints solo llaman a las funciones que hacen toda esta logica
vamos a usar schemas para no andar referenciando el gran cuerpo de datos a cada rato
"""

def verificar_credencial_empleado(usuario: str, db: Session):
    try:
        resultados = ejecutar_sp(db, "sp_ObtenerCredencialUsuario", Login=usuario)
        if not resultados:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="Usuario o correo no encontrado."
            )
        return resultados[0]
        
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error BD: {str(e.__dict__.get('orig', e))}"
        )

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
        

def verificar_credencial_usuario(usuario: str, db: Session):
    try:
        resultados = ejecutar_sp(db, "sp_ObtenerCredencialEmpleado", Login=usuario)
        if not resultados:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="Usuario o correo no encontrado."
            )
        return resultados[0]
        
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error BD: {str(e.__dict__.get('orig', e))}"
        )


def login_usuario(datos: LoginRes, db: Session):
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


def solicitud_usuario(
    db: Session,
    nombres: str,
    apellidos: str,
    fecha_nacimiento: date,
    correo: str,
    pais_id: int,
    usuario: str,
    password: str,
    codigo: str,
    telefono: str | None = None,
    minutos_validez: int = 10,
    max_intentos: int = 5,
):
    try:
        # 1 Generar hash de la contraseña
        hash_password = hasher(password)

        # 2 Ejecutar SP en base de datos
        resultado = obtener_solicitud_registro(
            db=db,
            nombres=nombres,
            apellidos=apellidos,
            fecha_nacimiento=fecha_nacimiento,
            correo=correo,
            pais_id=pais_id,
            usuario=usuario,
            hash_contrasena=hash_password,
            codigo=codigo,
            telefono=telefono,
            minutos_validez=minutos_validez,
            max_intentos=max_intentos,
        )

        # 3 Validar resultado de BD ANTES de enviar correo
        if not resultado:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No se pudo crear la solicitud de registro."
            )

        # 4 Enviar correo solo si la inserción en BD fue exitosa
        enviar_correo(nombres, correo, codigo, "registro")

        return {
            "message": "Solicitud de registro creada exitosamente.",
            "data": resultado[0] if isinstance(resultado, list) else resultado
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