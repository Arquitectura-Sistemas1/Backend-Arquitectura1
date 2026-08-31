import os
from dotenv import load_dotenv, find_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.engine import make_url

# Cargar variables de entorno del archivo .env
load_dotenv(find_dotenv())
DATABASE_URL_BASE = os.getenv("DATABASE_URL_BASE3") or os.getenv("DATABASE_URL3")

# Forzar la conexión a la base de datos 'master' para poder listar todo el catálogo del sistema
url_obj = make_url(DATABASE_URL_BASE)
url_master = url_obj.set(database="master")

# Crear el motor de conexión apuntando a 'master'
engine_master = create_engine(url_master, pool_pre_ping=True)

if __name__ == "__main__":
    print("=== INSPECTOR DE INSTANCIA SQL SERVER ===")
    print("Conectando al motor para listar las bases de datos activas...")
    
    try:
        with engine_master.connect() as connection:
            # Consulta estándar para obtener las bases de datos en línea
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
                # Formatear la fecha si existe en los metadatos del sistema
                creacion = fila.FechaCreacion.strftime("%Y-%m-%d %H:%M") if fila.FechaCreacion else "N/A"
                print(f"{nombre:<35} | {creacion:<20}")
                
    except Exception as e:
        print("\n❌ ERROR AL CONECTAR O LISTAR LAS BASES DE DATOS:")
        print(e)
