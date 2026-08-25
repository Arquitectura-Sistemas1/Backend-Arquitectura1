
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.core.crud import obtener_credencial_empleado, obtener_credencial_usuario
from app.core.database import get_db 
from app.funciones.psswds import hasher, comparar_hash

router = APIRouter(prefix="/auth", tags=["Credenciales"])


@router.post("/credencial-empleado", status_code=status.HTTP_200_OK)
def verificar_credencial_empleado(usuario: str, db: Session = Depends(get_db)):
  
    try:
        resultados = obtener_credencial_empleado(db, login=usuario)
        if not resultados:
            raise HTTPException(status_code=404, detail="Usuario o correo no encontrado.")
        
        # aca devuelve el primer registro con todas sus columnas originales
        return resultados[0]
        
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error BD: {str(e.__dict__.get('orig', e))}"
        )


@router.post("/credencial-usuario", status_code=status.HTTP_200_OK)
def verificar_credencial_usuario(usuario: str, db: Session = Depends(get_db)):

    try:
        resultados = obtener_credencial_usuario(db, login=usuario)
        if not resultados:
            raise HTTPException(status_code=404, detail="Usuario o correo no encontrado.")
            
        # este retornael primer registro con todas sus columnas originales
        return resultados[0]
        
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error BD: {str(e.__dict__.get('orig', e))}"
        )

@router.post("/login-usuario", status_code=status.HTTP_200_OK)
def login_usuario(usuario: str, password: str, db: Session = Depends(get_db)):

    try:
        resultados = obtener_credencial_usuario(db, login=usuario)
        if not resultados:
            raise HTTPException(status_code=404, detail="Usuario o correo no encontrado.")
        
        # aca devuelve el primer registro con todas sus columnas originales
        credencial = resultados[0]
        
        # Verificar la contraseña proporcionada con la contraseña almacenada
        if not comparar_hash(password, credencial['HashContrasena']):
            raise HTTPException(status_code=401, detail="Contraseña incorrecta.")
        
        return {"message": "Inicio de sesión exitoso." + resultados[0]['Nombre'] + " " + resultados[0]['ApellidoPaterno'] }
        
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error BD: {str(e.__dict__.get('orig', e))}"
        )