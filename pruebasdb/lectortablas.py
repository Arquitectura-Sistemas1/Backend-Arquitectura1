import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, MetaData, inspect
from sqlalchemy.engine import make_url  # <-- Importamos make_url
from sqlalchemy.orm import declarative_base, sessionmaker

NombreDb=input("Ingrese el nombre de la base de datos a la que desea conectarse: ")

# Carga las variables de entorno (.env o credenciales.env)
load_dotenv() 

# 1. Leemos la URL base del servidor (ej. mssql+pyodbc://usuario:pass@100.109.91.46,1433/...)
DATABASE_URL_BASE = os.getenv("DATABASE_URL_BASE")

# 2. Le inyectamos específicamente la base de datos "TiendaVideojuegosDB"
url_obj = make_url(DATABASE_URL_BASE)
DATABASE_URL = url_obj.set(database=NombreDb)

# 3. Creamos el engine apuntando a la BD específica
engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

if __name__ == "__main__":
    print("Conectando a SQL Server y cargando nombres de tablas de forma ligera...")
    
    try:
        # Inspector ligero para obtener tablas de TiendaVideojuegosDB
        inspector = inspect(engine)
        nombres_tablas = inspector.get_table_names()
        
        print(f"\n=== CONEXIÓN EXITOSA EN '{NombreDb}' ===")
        print(f"Total de tablas encontradas: {len(nombres_tablas)}")
        print("Tablas:")
        for tabla in nombres_tablas:
            print(f" - {tabla}")
            
    except Exception as e:
        print("\n=== ERROR DE CONEXIÓN ===")
        print(e)