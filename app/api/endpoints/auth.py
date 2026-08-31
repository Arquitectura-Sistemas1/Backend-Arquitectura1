
from fastapi import APIRouter, Depends, status, Request, Response  # <-- 1. Importa Request
from app.core.database import Session
from app.api.deps import get_db
from app.services.auth import login_usuario, solicitud_usuario, verificar_y_completar_registro
from app.core.limiter import limiter
from app.core.security import ACCESS_TOKEN_EXPIRE_MINUTES
from app.schemas.auth import (
    LoginRes, LoginReq, SolicitudUsuarioReq, SolicitudUsuarioRes, ConfirmaRegistroReq,
    ConfirmaRegistroRes
)
router = APIRouter(prefix="/auth", tags=["Auth"])




# aplicar el limitador al login y agregar 'request: Request'
@router.post("/login", status_code=status.HTTP_200_OK, response_model=LoginRes)
@limiter.limit("3/minute")  # este lmita a 3 intentos por minuto por IP
def login_usuario_endpoint(
    request: Request,
    response: Response,
    payload: LoginReq,
    db: Session = Depends(get_db)
):
    print(f"Intento de login desde la IP: {request.client.host}")
    resultado, token = login_usuario(payload, db)
    response.set_cookie(
        key="access_token",
        value=f"Bearer {token}",
        httponly=True,
        max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        samesite="lax",
        path="/"
    )
    return resultado

@router.post("/logout", status_code=status.HTTP_200_OK)
def logout_usuario(response: Response):
    response.delete_cookie(
        key="access_token",
        path="/",
        httponly=True,
        samesite="lax"
    )
    return {"message": "Sesión cerrada exitosamente"}

@router.post("/solicitud-usuario", status_code=status.HTTP_201_CREATED, response_model=SolicitudUsuarioRes)
@limiter.limit("3/hour")
def solicitud_usuario_endpoint(request: Request, datos : SolicitudUsuarioReq, db: Session = Depends(get_db)):
    return solicitud_usuario(db, datos)


@router.post("/confirmar-registro", status_code=status.HTTP_201_CREATED, response_model=ConfirmaRegistroRes)
@limiter.limit("2/minute")
def confirmar_registro_endpoint(request: Request, datos: ConfirmaRegistroReq, db: Session = Depends(get_db)):
    return verificar_y_completar_registro(datos, db)
