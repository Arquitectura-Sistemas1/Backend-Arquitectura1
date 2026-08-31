from datetime import date
from sqlalchemy.orm import Session
from app.core.database import ejecutar_sp, ejecutar_sp_commit
from app.schemas.inventario import VideojuegoCreate, VideojuegoGet
from app.externalservices.nubecloudi import subir_imagen
from fastapi import UploadFile

"vuelvo a indicar que esta es logica solo para llamar procedimientos almacenados"
"""
    @ClasificacionID      INT,
    @Titulo               NVARCHAR(200),
    @Descripcion          NVARCHAR(MAX) = NULL,
    @FechaLanzamiento     DATE = NULL,
    @NumeroJugadores      SMALLINT = 1,
    @Edicion              NVARCHAR(100) = NULL,
    @Idioma               NVARCHAR(80) = NULL,
    @GeneroID             INT = NULL,
    @DesarrolladoraID     INT = NULL,
    @PortadaURL           NVARCHAR(500) = NULL,
    @VideojuegoID         BIGINT OUTPUT,
    @PortadaID            BIGINT OUTPUT

"""

def cargar_videojuegos(db: Session, datos: VideojuegoGet):
    id = datos.id
    resultado = ejecutar_sp(db, "GetVideoGames", VideojuegoID=id)
    res = resultado[0]
    return {
    "id": res["VideojuegoID"],
    "titulo": res["Titulo"],
    "descripcion": res["Descripcion"],
    "fecha_lanzamiento": res["FechaLanzamiento"],
    "numero_jugadores": res["NumeroJugadores"],
    "edicion": res["Edicion"],
    "idioma": res["Idioma"],
    "clasificacion": {
        "id": res["ClasificacionID"],
        "codigo": res["ClasificacionCodigo"],
        "edad_minima": res["ClasificacionEdadMinima"],
        "descripcion": res["ClasificacionDescripcion"]
    },
    "genero": {
        "id": res["GeneroID"],
        "nombre": res["GeneroNombre"],
        "descripcion": res["GeneroDescripcion"]
    },
    "desarrolladora": {
        "id": res["DesarrolladoraID"],
        "nombre": res["DesarrolladoraNombre"],
        "sitio_web": res["DesarrolladoraSitioWeb"]
    },
    "portada": {
        "id": res["PortadaID"],
        "url": res["PortadaURL"]
    }
}
    

def crear_videojuego(db: Session,  file: UploadFile | None, datos: VideojuegoCreate):
    url_foto = None
    if file and file.filename:
        url_foto = subir_imagen(file)
    resultado = ejecutar_sp_commit(
        db, 
        "sp_CrearVideojuego", 
        ClasificacionID=datos.clasificacion_id, 
        Titulo=datos.titulo,
        Descripcion=datos.descripcion,
        FechaLanzamiento=datos.fecha_lanzamiento,
        NumeroJugadores=datos.numero_jugadores,
        Edicion=datos.edicion,
        Idioma=datos.idioma,
        GeneroID=datos.genero_id,
        DesarrolladoraID=datos.desarrolladora_id,
        PortadaURL= url_foto, #de momento se queda none porque no tengo aun peusto el tema de cloudinary
        VideojuegoID=None,
        PortadaID=None,
        )
    res = resultado[0]

    return {
                "videojuego_id": res["VideojuegoID"],
                "portada_id": res["PortadaID"]
            }