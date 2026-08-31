
from argon2 import PasswordHasher
from argon2.exceptions import VerificationError, VerifyMismatchError
from datetime import datetime, timedelta, timezone
from typing import Optional
import jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status, Request
from app.config import settings

ph = PasswordHasher()

def hasher (str: str):
    password = str
    res = ph.hash(password)
    return res

def comparar_hash (str: str, hash: str):
    password = str
    try:
        res = ph.verify(hash, password)
        return res
    except (VerifyMismatchError, VerificationError):
        return False


#aca las partes de los jwt

SECRET_KEY = settings.KEY_JWT
ALGORITHM = settings.JWT_ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

def crear_token_acceso(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Crea un JWT firmado con expiración
    
    """
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    # para signar claim de expiración 
    to_encode.update({"exp": expire})
    
    # Firmar token
    token_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return token_jwt


def decodificar_token(token: str) -> dict:
    """
    Decodifica y valida la firma y expiración del JWT
    tambien nza una excepción si el token es inválido o ha expirado
    
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="El token ha expirado. Por favor, inicia sesión nuevamente."
        )
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token de autenticación inválido."
        )


#  extraer el usuario desde la Cookie 
def obtener_payload_actual(request: Request) -> dict:
    """
    lee la cookie access_token
    valida el JWT y devuelve el payload
    """
    cookie_token = request.cookies.get("access_token")
    
    if not cookie_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No se encontró la cookie de sesión."
        )
    
    # Remover el prefijo bearer si existe
    token = cookie_token.replace("Bearer ", "")
    
    # validar el token y obtener payload
    payload = decodificar_token(token)
    return payload


def obtener_usuario_actual(request: Request) -> str:
    """
    lee la cookie access_token
    valida el JWT y devuelve el ID del usuario
    """
    payload = obtener_payload_actual(request)
    user_id: Optional[str] = payload.get("sub")
    
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido: falta información de usuario"
        )
        
    return user_id


def obtener_empleado_admin_actual(request: Request) -> dict:
    """
    valida que la cookie pertenezca a un empleado administrador
    """
    payload = obtener_payload_actual(request)
    user_id: Optional[str] = payload.get("sub")
    tipo_cuenta: Optional[str] = payload.get("tipo_cuenta")
    rol_id = payload.get("rol_id")

    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido: falta información de usuario"
        )

    if tipo_cuenta != "Empleado":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo los empleados pueden realizar esta acción."
        )

    try:
        rol_id = int(rol_id)
    except (TypeError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo los empleados administradores pueden realizar esta acción."
        )

    if rol_id != 1:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo los empleados administradores pueden realizar esta acción."
        )

    return payload
