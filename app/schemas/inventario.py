from datetime import date 
from pydantic import BaseModel, Field

class VideojuegoCreate(BaseModel):  # Sugerencia: nombrar como 'Create' o 'Request' indica su propósito de entrada
    clasificacion_id: int
    titulo: str = Field(..., max_length=200) # Coincide con NVARCHAR(200)
    descripcion: str | None = None
    fecha_lanzamiento: date | None = None
    numero_jugadores: int = Field(default=1, ge=1, le=100) # Mínimo 1 jugador, evita overflows
    edicion: str | None = Field(default=None, max_length=100)
    idioma: str | None = Field(default=None, max_length=80)
    genero_id: int | None = None
    desarrolladora_id: int | None = None

class VideojuegoResponse(BaseModel):
    videojuego_id: int
    portada_id: int

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
    @PortadaURL           NVARCHAR(500) = NULL, se genera en backend, no vienee del frontend nunca
    @VideojuegoID         BIGINT OUTPUT,
    @PortadaID            BIGINT OUTPUT

"""