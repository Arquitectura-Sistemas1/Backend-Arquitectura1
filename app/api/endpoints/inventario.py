
from fastapi import APIRouter, Depends, status
from app.core.database import Session
from app.api.deps import get_db
from app.core.security import obtener_usuario_actual
from app.services.inventario import crear_videojuego, cargar_videojuegos, listar_videojuegos_catalogo
from app.schemas.inventario import (
    VideojuegoResponse,
    VideojuegoCreate,
    VideoGameStrictResponse,
    VideojuegoGet,
    VideojuegoCatalogoResponse
)
from fastapi import UploadFile, File
from fastapi import FastAPI, Depends, status, Request # <-- Importar Request
from sqlalchemy.orm import Session


router = APIRouter(prefix="/inv", tags=["Inventario"]) #uohisdhasd

"""pasos para crear un endpoint
1. es definir esquema de informacion
    a. esquema de entrada (opr ejemplo loginreq: usuario string, pssw string)
    b. esquema de salida (por ejmplo loginres): mensaje string, usuario: usuarioinfo
si no hay esquemas y response model la solucitud se veria del tipo url/inv/login_arturo_123

cuando si hay esquemas y response model siempre se ve asi

solicitud: url/inv/login
body: {
    "usuario": "arturo_123",
    "pssw": "123"}
respuesta
    {mensaje, usuarioinfo}

2. vamos a definir si nustro endpoint requiere insercion de imformacion o no. de esta decision depende
el verbo http a usar (get, post, put, delete, ...) y tambien la funcion sp a usar (sp!=sp_commit)

3. definir tareas/funnciones que ejecuta el endpoint y enviar esa logica a una funcion en la capa services
    a. IMPORTANTE MODULARIZAR
4. definir la informacion que se ingresa a la funcion en capa services y asignarla en el endpoint principal

5. cargar los endpoints a router.py


"""

"""
reseteo contrasena (auth)

======================================
manana a la noche (8 pm)

arturo
definir inputs y outputs
verificar que esten los sp necesarios y si no estan, crearlos rapido


obtener paises (informacion) (aunque solo sirva para el usuario) dominick
obtener plataformas (informacion)


obtener generos (informacino) fernando
obtener clasificacion (informacion)


obtener region (queda pendiente cambio db) yeisson
obtener desarrolladora (queda pendiente cambio db)


ubtener metodos pago (imformacion) eduardo
obtener tarifas (informacion) (mandar a traer todas las tarifas existentes en db)



obtener descuentos (informacion) (mandar a biuscar todos los descuentos registrados en db) angel
obtener solicitudesDevolicion (informacion) manadar a buscar todas las solicitides de devolucioni/reembolso en db

=========================================

agregarpedidoitem (comercial) se encarga de agregar a la lista pedidoitem un videojuego asociado y el pedido actual
creadpedido (comercial) genera un registro en db sobre un nuevo pedido
procesarpedido (comercial) pasaria de fase de llenar un pedido a intentar el pago (hace factura y manda a tabla pedidos completados)
pagar/procesar pago (comercial ) llama a un metodo de pago y registra el apgo (simulando que se pago)
eliminarpedido
eliminiarpedidoitem

=============================
solicitardevolucion(gestion) (esto lo hace el cliente)
resolversolicitud (gestion) (esto lo hace el empleado de soporte)


ver como subir solo carpetas especificas en git 

"""


@router.get("/videojuegos", status_code=status.HTTP_200_OK, response_model=list[VideojuegoCatalogoResponse])
def listar_videojuegos_catalogo_endpoint(
    request: Request, # <-- Agregar este parámetro obligatorio para slowapi
    db: Session = Depends(get_db)
):
    return listar_videojuegos_catalogo(db)

@router.post("/crear-videojuego", status_code=status.HTTP_201_CREATED, response_model=VideojuegoResponse)
def crear_videojuego_endpoint(
    datos: VideojuegoCreate = Depends(VideojuegoCreate.as_form), # <-- Inyección directa del Schema
    file: UploadFile | None = File(None),
    db: Session = Depends(get_db),
    usuario_actual: str = Depends(obtener_usuario_actual)
):
    return crear_videojuego(db, file, datos)

@router.post("/buscar-videojuego", status_code=status.HTTP_200_OK, response_model=VideoGameStrictResponse)
def buscar_videojuego_endpoint(
    datos: VideojuegoGet,
    db: Session = Depends(get_db),
    usuario_actual: str = Depends(obtener_usuario_actual)
):
    return cargar_videojuegos(db, datos)
