from datetime import date
from sqlalchemy.orm import Session
from app.core.database import ejecutar_sp, ejecutar_sp_commit
from app.schemas.inventario import VideojuegoCreate, VideojuegoGet
from app.externalservices.nubecloudi import subir_imagen
from fastapi import UploadFile


def listar_videojuegos_catalogo(db: Session):
    resultado = ejecutar_sp(db, "GetVideoGames", VideojuegoID=None)
    
    lista = []
    for res in resultado:
        # Convertimos la fila a Mapping/Dict para habilitar el uso seguro de .get()
        data = dict(res._mapping) if hasattr(res, "_mapping") else dict(res)
        
        lista.append({
            "id": data.get("VideojuegoID") or data.get("id"),
            "titulo": data.get("Titulo") or data.get("titulo"),
            "descripcion": data.get("Descripcion") or data.get("descripcion"),
            "fecha_lanzamiento": data.get("FechaLanzamiento") or data.get("fecha_lanzamiento"),
            "numero_jugadores": data.get("NumeroJugadores") or data.get("numero_jugadores"),
            "edicion": data.get("Edicion") or data.get("edicion"),
            "idioma": data.get("Idioma") or data.get("idioma"),
            "clasificacion_id": data.get("ClasificacionID"),
            "clasificacion_nombre": data.get("ClasificacionNombre"),
            "genero_id": data.get("GeneroID"),
            "genero_nombre": data.get("GeneroNombre"),
            "desarrolladora_id": data.get("DesarrolladoraID"),
            "desarrolladora_nombre": data.get("DesarrolladoraNombre"),
            "portada_id": data.get("PortadaID"),
            "portada_url": data.get("PortadaURL"),
        })
        
    return lista

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
