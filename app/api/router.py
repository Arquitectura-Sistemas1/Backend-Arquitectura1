
from fastapi import APIRouter, Depends, status
from app.core.database import Session
from app.api.deps import get_db
from app.services.auth import verificar_credencial_empleado, verificar_credencial_usuario, login_usuario

router = APIRouter(prefix="/auth", tags=["Credenciales"])


@router.post("/credencial-empleado", status_code=status.HTTP_200_OK)
def verificar_credencial_empleado_endpoint(usuario: str, db: Session = Depends(get_db)):
    return verificar_credencial_empleado(usuario, db)


@router.post("/credencial-usuario", status_code=status.HTTP_200_OK)
def verificar_credencial_usuario_endpoint(usuario: str, db: Session = Depends(get_db)):
    return verificar_credencial_usuario(usuario, db)

    
@router.post("/login", status_code=status.HTTP_200_OK)
def login_usuario_endpoint(usuario: str, password: str, db: Session = Depends(get_db)):
    return login_usuario(usuario, password, db)