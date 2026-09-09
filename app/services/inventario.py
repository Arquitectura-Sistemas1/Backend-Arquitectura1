from datetime import date
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from sqlalchemy import text
from fastapi import HTTPException, UploadFile

from app.core.database import ejecutar_sp, ejecutar_sp_commit
from app.schemas.inventario import VideojuegoCreate, VideojuegoGet
from app.externalservices.nubecloudi import subir_imagen


def _mapear_videojuego(res: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "id": res.get("VideojuegoID") or res.get("id"),
        "titulo": res.get("Titulo") or res.get("titulo"),
        "descripcion": res.get("Descripcion") or res.get("descripcion"),
        "fecha_lanzamiento": res.get("FechaLanzamiento") or res.get("fecha_lanzamiento"),
        "num_jugadores": (
            res.get("Num_Jugadores")
            or res.get("NumJugadores")
            or res.get("NumeroJugadores")
            or 1
        ),
        "edicion": res.get("Edicion") or res.get("edicion"),
        "fecha_creacion": res.get("FechaCreacion") or res.get("fecha_creacion"),

        "plataforma": {
            "id": res.get("PlataformaID"),
            "nombre": res.get("PlataformaNombre")
        } if res.get("PlataformaID") is not None else None,

        "region": {
            "id": res.get("RegionID"),
            "nombre": res.get("RegionNombre")
        } if res.get("RegionID") is not None else None,

        "tarifa": {
            "id": res.get("TarifaID"),
            "precio_venta": res.get("PrecioVenta"),
            "precio_renta": res.get("PrecioRenta"),
            "duracion_renta_horas": res.get("DuracionRentaHoras")
        } if res.get("TarifaID") is not None else None,

        "descuento": {
            "id": res.get("DescuentoID"),
            "tipo": res.get("DescuentoTipo"),
            "valor": res.get("DescuentoValor"),
            "fecha_inicio": res.get("DescuentoFechaInicio"),
            "fecha_fin": res.get("DescuentoFechaFin")
        } if res.get("DescuentoID") is not None else None,

        "clasificacion": {
            "id": res.get("ClasificacionID"),
            "codigo": res.get("ClasificacionCodigo") or res.get("ClasificacionNombre"),
            "edad_minima": res.get("ClasificacionEdadMinima"),
            "descripcion": res.get("ClasificacionDescripcion")
        } if res.get("ClasificacionID") is not None else None,

        "genero": {
            "id": res.get("GeneroID"),
            "nombre": res.get("GeneroNombre"),
            "descripcion": res.get("GeneroDescripcion")
        } if res.get("GeneroID") is not None else None,

        "desarrolladora": {
            "id": res.get("DesarrolladoraID"),
            "nombre": res.get("DesarrolladoraNombre"),
            "sitio_web": res.get("DesarrolladoraSitioWeb")
        } if res.get("DesarrolladoraID") is not None else None,

        "portada": {
            "id": res.get("PortadaID"),
            "url": res.get("PortadaURL") or res.get("URL")
        } if (
            res.get("PortadaID") is not None
            or res.get("PortadaURL")
        ) else None
    }


def _mapear_catalogo(res: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "id": res.get("VideojuegoID"),
        "titulo": res.get("Titulo"),
        "descripcion": res.get("Descripcion"),
        "fecha_lanzamiento": res.get("FechaLanzamiento"),
        "num_jugadores": res.get("Num_Jugadores"),
        "edicion": res.get("Edicion"),

        "plataforma_id": res.get("PlataformaID"),
        "plataforma_nombre": res.get("PlataformaNombre"),

        "region_id": res.get("RegionID"),
        "region_nombre": res.get("RegionNombre"),

        "tarifa_id": res.get("TarifaID"),
        "precio_venta": res.get("PrecioVenta"),
        "precio_renta": res.get("PrecioRenta"),
        "duracion_renta_horas": res.get("DuracionRentaHoras"),

        "descuento_id": res.get("DescuentoID"),
        "descuento_tipo": res.get("DescuentoTipo"),
        "descuento_valor": res.get("DescuentoValor"),
        "descuento_fecha_inicio": res.get("DescuentoFechaInicio"),
        "descuento_fecha_fin": res.get("DescuentoFechaFin"),

        "clasificacion_id": res.get("ClasificacionID"),
        "clasificacion_nombre": res.get("ClasificacionCodigo"),

        "genero_id": res.get("GeneroID"),
        "genero_nombre": res.get("GeneroNombre"),

        "desarrolladora_id": res.get("DesarrolladoraID"),
        "desarrolladora_nombre": res.get("DesarrolladoraNombre"),

        "portada_id": res.get("PortadaID"),
        "portada_url": res.get("PortadaURL")
    }


def listar_videojuegos_catalogo(db: Session) -> List[Dict[str, Any]]:
    resultado = ejecutar_sp(db, "sp_listar_videojuegos_catalogo")

    if not resultado:
        return []

    return [
        _mapear_catalogo(
            dict(row._mapping) if hasattr(row, "_mapping") else dict(row)
        )
        for row in resultado
    ]

def cargar_videojuegos(db: Session, datos: Any) -> Dict[str, Any]:
    v_id = datos.id if hasattr(datos, "id") else (datos.get("id") if isinstance(datos, dict) else None)
    
    resultado = ejecutar_sp(db, "GetVideoGames", VideojuegoID=v_id)
    
    if not resultado:
        raise HTTPException(
            status_code=404,
            detail=f"No se encontró el videojuego con ID {v_id}"
        )
        
    row = resultado[0]
    res = dict(row._mapping) if hasattr(row, "_mapping") else dict(row)

    # Reutilizamos la misma función de mapeo
    return _mapear_videojuego(res)



def crear_videojuego(db: Session, file: Optional[UploadFile], datos: Any):
    # Convertir Pydantic o FormData a dict
    if hasattr(datos, "model_dump"):
        datos_dict = datos.model_dump()
    elif hasattr(datos, "dict"):
        datos_dict = datos.dict()
    elif isinstance(datos, dict):
        datos_dict = datos
    else:
        datos_dict = getattr(datos, "__dict__", {})

    # 1. Subir a Cloudinary si viene imagen
    portada_url = None
    if file and file.filename:
        res_nube = subir_imagen(file)
        if isinstance(res_nube, dict):
            portada_url = res_nube.get("secure_url") or res_nube.get("url")
        elif isinstance(res_nube, str):
            portada_url = res_nube

    # 2. Mapear parámetros EXACTAMENTE con los nombres del SP en SQL Server
    parametros = {
        "PlataformaID": datos_dict.get("plataforma_id"),
        "ClasificacionID": datos_dict.get("clasificacion_id"),
        "RegionID": datos_dict.get("region_id"),
        "TarifaID": datos_dict.get("tarifa_id"),
        "DescuentoID": datos_dict.get("descuento_id"),
        "Titulo": datos_dict.get("titulo"),
        "Descripcion": datos_dict.get("descripcion"),
        "FechaLanzamiento": datos_dict.get("fecha_lanzamiento"),
        "Num_Jugadores": datos_dict.get("num_jugadores") or 1,
        "Edicion": datos_dict.get("edicion"),
        "GeneroID": datos_dict.get("genero_id"),
        "DesarrolladoraID": datos_dict.get("desarrolladora_id"),
        "PortadaURL": portada_url,
        "VideojuegoID": None,  # <-- Se manda None para que pase el check de pymssql
        "PortadaID": None      # <-- Se manda None para que pase el check de pymssql
    }

    # 3. Ejecutar el SP sp_CrearVideojuego
    resultado = ejecutar_sp_commit(db, "sp_CrearVideojuego", **parametros)

    if not resultado:
        raise HTTPException(
            status_code=500,
            detail="El Stored Procedure 'sp_CrearVideojuego' no devolvió ningún resultado."
        )

    # 4. Extraer VideojuegoID y PortadaID
    primera_fila = resultado[0]
    data = dict(primera_fila._mapping) if hasattr(primera_fila, "_mapping") else dict(primera_fila)

    videojuego_id = data.get("VideojuegoID") or data.get("id")
    portada_id = data.get("PortadaID")

    if videojuego_id is None:
        raise HTTPException(
            status_code=500,
            detail="No se pudo obtener el ID del videojuego recién creado."
        )

    return {
        "mensaje": "Videojuego creado exitosamente",
        "videojuego_id": int(videojuego_id),
        "portada_id": int(portada_id) if portada_id else None,
        "portada_url": portada_url
    }