import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, MetaData, inspect
from sqlalchemy.engine import make_url 
from sqlalchemy.orm import declarative_base, sessionmaker


load_dotenv() 


DATABASE_URL_BASE = os.getenv("DATABASE_URL_BASE")


url_obj = make_url(DATABASE_URL_BASE)
DATABASE_URL = url_obj.set(database="tempdb")


engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

if __name__ == "__main__":
    print("Conectando a SQL Server y cargando nombres de tablas de forma ligera...")
    
    try:
 
        inspector = inspect(engine)
        nombres_tablas = inspector.get_table_names()
        
        print("\n=== CONEXIÓN EXITOSA EN 'TiendaVideojuegosDB' ===")
        print(f"Total de tablas encontradas: {len(nombres_tablas)}")
        print("Tablas:")
        for tabla in nombres_tablas:
            print(f" - {tabla}")
            
    except Exception as e:
        print("\n=== ERROR DE CONEXIÓN ===")
        print(e)