
from fastapi import APIRouter, Depends, status
from app.core.database import Session
from app.api.deps import get_db
from app.services.auth import verificar_credencial_empleado, verificar_credencial_usuario, login_usuario, solicitud_usuario, verificar_registro, registrar_usuario_final
from app.utils.codesgen import generar_codigo_verificacion
from datetime import date
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

@router.post("/solicitud-usuario", status_code=status.HTTP_201_CREATED)
def solicitud_usuario_endpoint(
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
def confirmar_registro_endpoint(
    usuario: str,
    codigo: str,
    db: Session = Depends(get_db)
):
    # 1. Ejecutar la verificación del código
    res_verificacion = verificar_registro(usuario=usuario, code=codigo, db=db)
    
    # 2. Extraer el SolicitudRegistroID obtenido del SP
    solicitud_id = res_verificacion.get("SolicitudRegistroID")
    
    # 3. Ejecutar la creación final del usuario en la base de datos
    return registrar_usuario_final(solicitud_id=solicitud_id, db=db)