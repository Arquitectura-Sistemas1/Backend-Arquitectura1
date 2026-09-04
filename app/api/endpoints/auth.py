
from fastapi import APIRouter, Depends, status, Request, Response  # <-- 1. Importa Request
from app.core.database import Session
from app.api.deps import get_db
from app.services.auth import login_usuario, solicitud_usuario, verificar_y_completar_registro, registrar_empleado
from app.core.limiter import limiter
from app.core.security import ACCESS_TOKEN_EXPIRE_MINUTES, obtener_empleado_admin_actual, obtener_payload_actual
from app.schemas.auth import (
    LoginRes, LoginReq, SolicitudUsuarioReq, SolicitudUsuarioRes, ConfirmaRegistroReq,
    ConfirmaRegistroRes, RegistrarEmpleadoReq, RegistrarEmpleadoRes
)
router = APIRouter(prefix="/auth", tags=["Auth"])
from fastapi.responses import RedirectResponse


#post (insercion), get (obtener informacion ), put (actualizar) delete (eliminar)


#solicitar-reseteo-contrasena



# aplicar el limitador al login y agregar 'request: Request'
#general
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
        samesite="none",
        secure=True,
        path="/"
    )
    return resultado

#es general
@router.post("/logout", status_code=status.HTTP_200_OK)
def logout_usuario(response: Response):
    response.delete_cookie(
        key="access_token",
        path="/",
        httponly=True,
        samesite="none",
        secure=True
    )
    return {"message": "Sesión cerrada exitosamente"}

@router.post("/solicitud-usuario", status_code=status.HTTP_201_CREATED, response_model=SolicitudUsuarioRes)
@limiter.limit("3/hour")
def solicitud_usuario_endpoint(request: Request, datos : SolicitudUsuarioReq, db: Session = Depends(get_db)):
    return solicitud_usuario(db, datos)

#corresponde a empleados, no a clientes
@router.post("/registrar-empleado", status_code=status.HTTP_201_CREATED, response_model=RegistrarEmpleadoRes)
def registrar_empleado_endpoint(
    datos: RegistrarEmpleadoReq,
    db: Session = Depends(get_db),
    empleado_admin: dict = Depends(obtener_empleado_admin_actual)
):
    return registrar_empleado(db, datos)

#corresponde solo a clientes
@router.post("/confirmar-registro", status_code=status.HTTP_201_CREATED, response_model=ConfirmaRegistroRes)
@limiter.limit("2/minute")
def confirmar_registro_endpoint(request: Request, datos: ConfirmaRegistroReq, db: Session = Depends(get_db)):
    return verificar_y_completar_registro(datos, db)


@router.get("/me", status_code=status.HTTP_200_OK)
def obtener_usuario_actual_endpoint(request: Request):
    """Devuelve el payload del JWT guardado en la cookie `access_token`.

    Útil para que el frontend verifique si el usuario tiene sesión activa sin exponer el token.
    """
    payload = obtener_payload_actual(request)
    return {"usuario": payload}


@router.get("/me/redirect")
def obtener_usuario_actual_redirect(request: Request):
    """Redirige al frontend según el estado de la sesión.

    - Si la cookie `access_token` es válida redirige a `/dashboard` del frontend.
    - Si no es válida redirige a `/login`.
    """
    frontend_base = "https://luxury-roster-uncouth.ngrok-free.dev"
    try:
        _ = obtener_payload_actual(request)
        return RedirectResponse(url=f"{frontend_base}")
    except Exception:
        return RedirectResponse(url=f"{frontend_base}/login")
