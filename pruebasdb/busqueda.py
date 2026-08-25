import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.engine import make_url

load_dotenv() 

DATABASE_URL_BASE = os.getenv("DATABASE_URL_BASE") or os.getenv("DATABASE_URL")

url_obj = make_url(DATABASE_URL_BASE)
url_master = url_obj.set(database="master")

engine = create_engine(url_master, pool_pre_ping=True)

if __name__ == "__main__":
    print("Conectando a SQL Server y obteniendo información de las bases de datos...")
    
    try:
        with engine.connect() as connection:
            # Consulta estándar sin requerir permisos de rendimiento
            query = text("""
                SELECT 
                    name AS Nombre,
                    create_date AS FechaCreacion
                FROM sys.databases
                WHERE state_desc = 'ONLINE'
                ORDER BY name;
            """)
            
            resultado = connection.execute(query)
            filas = resultado.fetchall()
            
            print("\n=== CONEXIÓN EXITOSA ===")
            print(f"Total de bases de datos encontradas: {len(filas)}\n")
            print(f"{'Base de Datos':<35} | {'Fecha Creación':<20}")
            print("-" * 60)
            
            for fila in filas:
                nombre = fila.Nombre
                creacion = fila.FechaCreacion.strftime("%Y-%m-%d %H:%M") if fila.FechaCreacion else "N/A"
                print(f"{nombre:<35} | {creacion:<20}")
                
    except Exception as e:
        print("\n=== ERROR DE CONEXIÓN ===")
        print(e)