import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.engine import make_url
from sqlalchemy.orm import declarative_base, sessionmaker

load_dotenv() 

DATABASE_URL2 = os.getenv("DATABASE_URL2")

url_obj = make_url(DATABASE_URL2)
nombre_db = url_obj.database

engine = create_engine(DATABASE_URL2, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

if __name__ == "__main__":
    print(f"Conectando a '{nombre_db}'...\n")
    
    try:
        inspector = inspect(engine)
        
        nombres_tablas = inspector.get_table_names()
        print(f"=== ESTRUCTURA DE LA BASE DE DATOS '{nombre_db}' ===")
        print(f"Total de tablas encontradas: {len(nombres_tablas)}\n")
        
        for tabla in nombres_tablas:
            print(f"--- TABLA: {tabla} ---")
            columnas = inspector.get_columns(tabla)
            pk_constraint = inspector.get_pk_constraint(tabla)
            pk_nombres = pk_constraint.get("constrained_columns", [])
            
            print(f"{'Columna':<30} | {'Tipo de Dato':<20} | {'Nulo?':<8} | {'Clave'}")
            print("-" * 70)
            
            for col in columnas:
                nombre_col = col['name']
                tipo_dato = str(col['type'])
                es_nulo = "SÍ" if col['nullable'] else "NO"
                es_pk = "PK" if nombre_col in pk_nombres else ""
                
                print(f"{nombre_col:<30} | {tipo_dato:<20} | {es_nulo:<8} | {es_pk}")
            print("\n")
            
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
            
            print(f"=== PROCEDIMIENTOS ALMACENADOS ===")
            print(f"Total de procedimientos encontrados: {len(procedimientos)}")
            if procedimientos:
                for sp in procedimientos:
                    print(f" - {sp.Esquema}.{sp.Nombre}")
            else:
                print("No se encontraron procedimientos almacenados en esta BD.")
            
    except Exception as e:
        print("\n=== ERROR DE CONEXIÓN O CONSULTA ===")
        print(e)