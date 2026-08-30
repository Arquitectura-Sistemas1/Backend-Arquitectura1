import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

# 1. Cargar variables de entorno desde el .env
load_dotenv()

DATABASE_URL2 = os.getenv("DATABASE_URL2")

if not DATABASE_URL2:
    raise ValueError("No se encontró la variable DATABASE_URL2 en el archivo .env")

# 2. Crear el engine para la ejecución
engine = create_engine(DATABASE_URL2, pool_pre_ping=True)

# 3. Defino la consulta SQL del SP corregido
sp_sql = """
CREATE OR ALTER PROCEDURE dbo.sp_CrearVideojuego
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
AS
BEGIN
    SET NOCOUNT ON;
    SET XACT_ABORT ON;

    SET @VideojuegoID = NULL;
    SET @PortadaID = NULL;

    /* Validaciones básicas */
    IF NULLIF(LTRIM(RTRIM(@Titulo)), N'') IS NULL
    BEGIN
        RAISERROR(N'El título del videojuego es obligatorio.', 16, 1);
        RETURN;
    END;

    IF @NumeroJugadores < 1
    BEGIN
        RAISERROR(N'El número de jugadores debe ser mayor o igual a 1.', 16, 1);
        RETURN;
    END;

    IF NOT EXISTS
    (
        SELECT 1
        FROM dbo.Clasificacion
        WHERE ID = @ClasificacionID
    )
    BEGIN
        RAISERROR(N'La clasificación indicada no existe.', 16, 1);
        RETURN;
    END;

    IF @GeneroID IS NOT NULL
       AND NOT EXISTS
       (
           SELECT 1
           FROM dbo.Genero
           WHERE ID = @GeneroID
       )
    BEGIN
        RAISERROR(N'El género indicado no existe.', 16, 1);
        RETURN;
    END;

    IF @DesarrolladoraID IS NOT NULL
       AND NOT EXISTS
       (
           SELECT 1
           FROM dbo.Desarrolladora
           WHERE ID = @DesarrolladoraID
       )
    BEGIN
        RAISERROR(N'La desarrolladora indicada no existe.', 16, 1);
        RETURN;
    END;

    IF @PortadaURL IS NOT NULL
       AND NULLIF(LTRIM(RTRIM(@PortadaURL)), N'') IS NULL
    BEGIN
        RAISERROR(N'La URL de portada no puede estar vacía.', 16, 1);
        RETURN;
    END;

    BEGIN TRANSACTION;

    BEGIN TRY
        INSERT INTO dbo.Videojuego
        (
            ClasificacionID,
            Titulo,
            Descripcion,
            FechaLanzamiento,
            NumeroJugadores,
            Edicion,
            Idioma
        )
        VALUES
        (
            @ClasificacionID,
            LTRIM(RTRIM(@Titulo)),
            @Descripcion,
            @FechaLanzamiento,
            @NumeroJugadores,
            @Edicion,
            @Idioma
        );

        SET @VideojuegoID = CONVERT(BIGINT, SCOPE_IDENTITY());

        /* Relación opcional con género */
        IF @GeneroID IS NOT NULL
        BEGIN
            INSERT INTO dbo.VideojuegoGenero
            (
                VideojuegoID,
                GeneroID
            )
            VALUES
            (
                @VideojuegoID,
                @GeneroID
            );
        END;

        /* Relación opcional con desarrolladora */
        IF @DesarrolladoraID IS NOT NULL
        BEGIN
            INSERT INTO dbo.VideojuegoDesarrolladora
            (
                VideojuegoID,
                DesarrolladoraID
            )
            VALUES
            (
                @VideojuegoID,
                @DesarrolladoraID
            );
        END;

        /* Portada inicial opcional */
        IF NULLIF(LTRIM(RTRIM(@PortadaURL)), N'') IS NOT NULL
        BEGIN
            INSERT INTO dbo.Portada
            (
                VideojuegoID,
                URL
            )
            VALUES
            (
                @VideojuegoID,
                LTRIM(RTRIM(@PortadaURL))
            );

            SET @PortadaID = CONVERT(BIGINT, SCOPE_IDENTITY());
        END;

        COMMIT TRANSACTION;

        /* RETORNO EXPLÍCITO PARA PYTHON */
        SELECT 
            @VideojuegoID AS VideojuegoID, 
            @PortadaID AS PortadaID;

    END TRY
    BEGIN CATCH
        IF @@TRANCOUNT > 0
            ROLLBACK TRANSACTION;

        DECLARE @ErrorMessage NVARCHAR(4000) = ERROR_MESSAGE();
        DECLARE @ErrorSeverity INT = ERROR_SEVERITY();
        DECLARE @ErrorState INT = ERROR_STATE();

        RAISERROR(@ErrorMessage, @ErrorSeverity, @ErrorState);
        RETURN;
    END CATCH;
END;
"""

def actualizar_sp():
    print("Conectando a la base de datos...")
    with engine.begin() as conn:
        conn.execute(text(sp_sql))
    print("¡Procedimiento dbo.sp_CrearVideojuego actualizado con éxito!")

if __name__ == "__main__":
    actualizar_sp()