
from fastapi import APIRouter, Depends, status, Request  # <-- 1. Importa Request
from app.core.database import Session
from app.api.deps import get_db
from app.services.auth import verificar_credencial_empleado, verificar_credencial_usuario, login_usuario, solicitud_usuario, verificar_registro, registrar_usuario_final
from app.utils.codesgen import generar_codigo_verificacion
from datetime import date
from app.core.limiter import limiter
 # oihdioasdnas
router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/credencial-empleado", status_code=status.HTTP_200_OK)
def verificar_credencial_empleado_endpoint(usuario: str, db: Session = Depends(get_db)):
    return verificar_credencial_empleado(usuario, db)


@router.post("/credencial-usuario", status_code=status.HTTP_200_OK)
def verificar_credencial_usuario_endpoint(usuario: str, db: Session = Depends(get_db)):
    return verificar_credencial_usuario(usuario, db)


# aplicar el limitador al login y agregar 'request: Request'
@router.post("/login", status_code=status.HTTP_200_OK)
@limiter.limit("3/minute")  # este lmita a 3 intentos por minuto por IP
def login_usuario_endpoint(request: Request, usuario: str, password: str, db: Session = Depends(get_db)):
    print(f"Intento de login desde la IP: {request.client.host}")
    return login_usuario(usuario, password, db)


@router.post("/solicitud-usuario", status_code=status.HTTP_201_CREATED)
@limiter.limit("3/hour")
def solicitud_usuario_endpoint(
    request: Request,
    nombres: str,
    apellidos: str,
    fecha_nacimiento: date,
    correo: str,
    pais_id: int,
    usuario: str,
    password: str,
    telefono: str | None = None,
    db: Session = Depends(get_db)
):
    return solicitud_usuario(
        db=db,
        nombres=nombres,
        apellidos=apellidos,
        fecha_nacimiento=fecha_nacimiento,
        correo=correo,
        pais_id=pais_id,
        usuario=usuario,
        password=password,
        codigo=generar_codigo_verificacion(),
        telefono=telefono
    )

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