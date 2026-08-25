# En: app/api/router.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.core.crud import obtener_credencial_empleado, obtener_credencial_usuario
from app.core.database import get_db 

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
