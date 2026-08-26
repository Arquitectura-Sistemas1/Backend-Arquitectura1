import os
from dotenv import load_dotenv, find_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.engine import make_url

load_dotenv(find_dotenv())

DATABASE_URL = os.getenv("DATABASE_URL2") or os.getenv("DATABASE_URL")
url_obj = make_url(DATABASE_URL)
nombre_db = url_obj.database

engine = create_engine(DATABASE_URL, pool_pre_ping=True)

# Construir ruta relativa dinámica basada en la posición de creacion.py
directorio_actual = os.path.dirname(__file__)
ARCHIVO_SQL = os.path.join(directorio_actual, "11_RegistroVerificacionUsuarios.sql")

if __name__ == "__main__":
    print(f"Ejecutando migración en la base de datos '{nombre_db}'...\n")
    
    try:
        if not os.path.exists(ARCHIVO_SQL):
            print(f"Error: No se encontró el archivo '{ARCHIVO_SQL}'.")
            exit(1)

        with open(ARCHIVO_SQL, "r", encoding="utf-8") as f:
            contenido_sql = f.read()

        bloques_sql = [b.strip() for b in contenido_sql.split("GO") if b.strip()]

        with engine.connect() as conn:
            for bloque in bloques_sql:
                lines = [line for line in bloque.splitlines() if not line.strip().upper().startswith("USE ")]
                sql_limpio = "\n".join(lines).strip()
                
                if sql_limpio:
                    conn.execute(text(sql_limpio))
                    conn.commit()

        print("=== ¡MIGRACIÓN COMPLETADA EXITOSAMENTE! ===")
        print(f"Se crearon/actualizaron las tablas y procedimientos en '{nombre_db}'.")

    except Exception as e:
        print("\n=== ERROR DURANTE LA EJECUCIÓN ===")
        print(e)