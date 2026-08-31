import os
from dotenv import load_dotenv, find_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.engine import make_url

load_dotenv(find_dotenv())

DATABASE_URL = os.getenv("DB_RESPALDO") or os.getenv("DATABASE_URL")
url_obj = make_url(DATABASE_URL)
nombre_db = url_obj.database

engine = create_engine(DATABASE_URL, pool_pre_ping=True)

directorio_actual = os.path.dirname(__file__)
ARCHIVO_SQL = os.path.join(directorio_actual, "01_CrearBaseDatos.sql")

if __name__ == "__main__":
    print(f"Preparando restablecimiento limpio en la base de datos '{nombre_db}'...\n")
    
    try:
        if not os.path.exists(ARCHIVO_SQL):
            print(f"Error: No se encontró el archivo '{ARCHIVO_SQL}'.")
            exit(1)

        with open(ARCHIVO_SQL, "r", encoding="utf-8") as f:
            lineas_archivo = f.readlines()

        bloques_sql = []
        bloque_actual = []

        for linea in lineas_archivo:
            linea_trim = linea.strip()
            
            # Detectar el comando GO de SQL Server (ignorando mayúsculas/minúsculas)
            if linea_trim.upper() == "GO":
                if bloque_actual:
                    sql_bloque = "\n".join(bloque_actual).strip()
                    if sql_bloque:
                        bloques_sql.append(sql_bloque)
                    bloque_actual = []
            else:
                # Omitir sentencias USE si llegara a haber alguna colada
                if not linea_trim.upper().startswith("USE "):
                    bloque_actual.append(linea)

        # Agregar el último bloque si el archivo no terminaba en GO
        if bloque_actual:
            sql_bloque = "\n".join(bloque_actual).strip()
            if sql_bloque:
                bloques_sql.append(sql_bloque)

        with engine.connect() as conn:
            print(f"Ejecutando {len(bloques_sql)} bloques de comandos SQL...")
            for idx, bloque in enumerate(bloques_sql, 1):
                conn.execute(text(bloque))
                conn.commit()

        print("\n=== ¡MIGRACIÓN COMPLETADA EXITOSAMENTE! ===")
        print(f"Se estructuró la base de datos '{nombre_db}' correctamente.")

    except Exception as e:
        print("\n=== ERROR DURANTE LA EJECUCIÓN ===")
        print(e)