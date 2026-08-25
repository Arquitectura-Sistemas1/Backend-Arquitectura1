import os
from dotenv import load_dotenv, find_dotenv
from sqlalchemy import create_engine, MetaData, inspect, text
from sqlalchemy.engine import make_url
from sqlalchemy.orm import declarative_base, sessionmaker

NombreDb = input("Ingrese el nombre de la base de datos a la que desea conectarse: ")

# Carga las variables de entorno (.env)
load_dotenv(find_dotenv())
# 1. Leemos la URL base del servidor
DATABASE_URL_BASE = os.getenv("DATABASE_URL_BASE") or os.getenv("DATABASE_URL")

# 2. Le inyectamos la base de datos ingresada por la consola
url_obj = make_url(DATABASE_URL_BASE)
DATABASE_URL = url_obj.set(database=NombreDb)

# 3. Creamos el engine
engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

if __name__ == "__main__":
    print(f"Conectando a '{NombreDb}'...")
    
    try:
        # --- TABLAS ---
        inspector = inspect(engine)
        nombres_tablas = inspector.get_table_names()
        
        print(f"\n=== CONEXIÓN EXITOSA EN '{NombreDb}' ===")
        print(f"Total de tablas encontradas: {len(nombres_tablas)}")
        print("Tablas:")
        for tabla in nombres_tablas:
            print(f" - {tabla}")
            
        # --- PROCEDIMIENTOS ALMACENADOS ---
        with engine.connect() as connection:
            query_sp = text("""
                SELECT 
                    SCHEMA_NAME(schema_id) AS Esquema,
                    name AS Nombre
                FROM sys.procedures
                ORDER BY Esquema, Nombre;
            """)
            resultado = connection.execute(query_sp)
            procedimientos = resultado.fetchall()
            
            print(f"\nTotal de procedimientos almacenados: {len(procedimientos)}")
            if procedimientos:
                print("Procedimientos Almacenados:")
                for sp in procedimientos:
                    print(f" - {sp.Esquema}.{sp.Nombre}")
            else:
                print("No se encontraron procedimientos almacenados en esta BD.")
            
    except Exception as e:
        print("\n=== ERROR DE CONEXIÓN O CONSULTA ===")
        print(e)