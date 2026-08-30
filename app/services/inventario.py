from datetime import date
from sqlalchemy.orm import Session
from app.core.database import ejecutar_sp, ejecutar_sp_commit
from app.schemas.inventario import VideojuegoCreate, VideojuegoResponse

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
def crear_videojuego(db: Session, datos: VideojuegoCreate):

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
        PortadaURL= None, #de momento se queda none porque no tengo aun peusto el tema de cloudinary
        VideojuegoID=None,
        PortadaID=None,
        )
    return {
        "videojuego_id": resultado.get("VideojuegoID"),
        "portada_id": resultado.get("PortadaID")
    }