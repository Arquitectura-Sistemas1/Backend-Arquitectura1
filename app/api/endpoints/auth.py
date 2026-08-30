
from fastapi import APIRouter, Depends, status, Request  # <-- 1. Importa Request
from app.core.database import Session
from app.api.deps import get_db
from app.services.auth import login_usuario, solicitud_usuario, verificar_registro, registrar_usuario_final
from app.utils.codesgen import generar_codigo_verificacion
from datetime import date
from app.core.limiter import limiter
from app.schemas.auth import LoginRes, LoginReq, SolicitudUsuarioReq, SolicitudUsuarioRes

router = APIRouter(prefix="/auth", tags=["Auth"])




# aplicar el limitador al login y agregar 'request: Request'
@router.post("/login", status_code=status.HTTP_200_OK, response_model=LoginRes)
@limiter.limit("3/minute")  # este lmita a 3 intentos por minuto por IP
def login_usuario_endpoint(request: Request, payload: LoginReq, db: Session = Depends(get_db)):
    print(f"Intento de login desde la IP: {request.client.host}")
    return login_usuario(payload, db)


@router.post("/solicitud-usuario", status_code=status.HTTP_201_CREATED, response_model=SolicitudUsuarioRes)
@limiter.limit("3/hour")
def solicitud_usuario_endpoint(request: Request, datos : SolicitudUsuarioReq, db: Session = Depends(get_db)):
    return solicitud_usuario(db, datos)


@router.post("/confirmar-registro", status_code=status.HTTP_201_CREATED)
@limiter.limit("2/minute")
def confirmar_registro_endpoint(
     request: Request,
    usuario: str,
    codigo: str,
    db: Session = Depends(get_db)
):

    res_verificacion = verificar_registro(usuario=usuario, code=codigo, db=db)
    solicitud_id = res_verificacion.get("SolicitudRegistroID")
    return registrar_usuario_final(solicitud_id=solicitud_id, db=db)