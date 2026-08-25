
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

    
@router.post("/login", status_code=status.HTTP_200_OK)
def login_usuario(usuario: str, password: str, db: Session = Depends(get_db)):
    
 
    try:
        resultados_usuario = obtener_credencial_usuario(db, login=usuario)
        
        if not resultados_usuario:
            raise ValueError("No encontrado en usuarios")            
        credencial = resultados_usuario[0]

        if not comparar_hash(password, credencial['HashContrasena']):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Contraseña incorrecta.")
        

        return {
            "tipo_cuenta": "usuario",
            "message": f"Inicio de sesión exitoso, usuario: {credencial['Usuario']}",
            "data": {
                "UsuarioID": credencial["UsuarioID"],
                "Correo": credencial["Correo"]
            }
        }
        
    except (SQLAlchemyError, ValueError, IndexError):

        try:
            resultados_empleado = obtener_credencial_empleado(db, login=usuario)
            

            if not resultados_empleado:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, 
                    detail="Usuario o correo no encontrado en el sistema."
                )
            
            credencial = resultados_empleado[0]
            

            if not comparar_hash(password, credencial['HashContrasena']):
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Contraseña incorrecta.")
            
            return {
                "tipo_cuenta": "empleado",
                "message": f"Inicio de sesión exitoso, empleado: {credencial['Usuario']}",
                "data": {
                    "EmpleadoID": credencial["EmpleadoID"],
                    "Correo": credencial["Correo"],
                    "RolID": credencial["RolID"]
                }
            }
            
        except SQLAlchemyError as e:

            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error BD en consulta de empleados: {str(e.__dict__.get('orig', e))}"
            )