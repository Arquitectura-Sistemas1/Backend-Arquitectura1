from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.crud.auth import obtener_credencial_empleado, obtener_credencial_usuario
from app.core.security import hasher, comparar_hash

def verificar_credencial_empleado(usuario: str, db: Session):
    try:
        resultados = obtener_credencial_empleado(db, login=usuario)
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

def verificar_credencial_usuario(usuario: str, db: Session):
    try:
        resultados = obtener_credencial_usuario(db, login=usuario)
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

def login_usuario(usuario: str, password: str, db: Session):
    try:
        # 1. Buscar en la tabla de usuarios
        resultados_usuario = obtener_credencial_usuario(db, login=usuario)
        
        if resultados_usuario:
            credencial = resultados_usuario[0]
            if not comparar_hash(password, credencial['HashContrasena']):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED, 
                    detail="Contraseña incorrecta."
                )
            return {
                "tipo_cuenta": "usuario",
                "message": f"Inicio de sesión exitoso, usuario: {credencial['Usuario']}",
                "data": {
                    "UsuarioID": credencial["UsuarioID"],
                    "Correo": credencial["Correo"]
                }
            }

        # 2. Si no existe como usuario, buscar en la tabla de empleados
        resultados_empleado = obtener_credencial_empleado(db, login=usuario)
        
        if resultados_empleado:
            credencial = resultados_empleado[0]
            if not comparar_hash(password, credencial['HashContrasena']):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED, 
                    detail="Contraseña incorrecta."
                )
            return {
                "tipo_cuenta": "empleado",
                "message": f"Inicio de sesión exitoso, empleado: {credencial['Usuario']}",
                "data": {
                    "EmpleadoID": credencial["EmpleadoID"],
                    "Correo": credencial["Correo"],
                    "RolID": credencial["RolID"]
                }
            }

        # 3. Si no existe en ninguno
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Usuario o correo no encontrado en el sistema."
        )

    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error BD en consulta de credenciales: {str(e.__dict__.get('orig', e))}"
        )