import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
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
    print(f"Conectando a '{nombre_db}' para inspeccionar registros...\n")
    
    # Nombres exactos de las 4 tablas
    tablas_objetivo = [
        "SolicitudRegistroUsuario",
        "CodigoRegistro",
        "Usuario",
        "CredencialUsuario"
    ]
    
    try:
        print(f"=== MUESTRA DE DATOS DE LA BASE DE DATOS '{nombre_db}' ===")
        print(f"Total de tablas a consultar: {len(tablas_objetivo)}\n")
        
        with engine.connect() as connection:
            for tabla in tablas_objetivo:
                print(f"==========================================")
                print(f"TABLA: {tabla}")
                print(f"==========================================")
                
                query_conteo = text(f"SELECT COUNT(*) FROM [{tabla}]")
                total_registros = connection.execute(query_conteo).scalar()
                print(f"Total de registros: {total_registros}")
                
                if total_registros > 0:
                    query_datos = text(f"SELECT TOP 10 * FROM [{tabla}]")
                    resultado = connection.execute(query_datos)
                    
                    columnas = resultado.keys()
                    filas = resultado.fetchall()
                    
                    header = " | ".join(columnas)
                    print("\nPrimeros registros (hasta 10):")
                    print(header)
                    print("-" * len(header))
                    
                    for fila in filas:
                        valores = [str(valor) if valor is not None else "NULL" for valor in fila]
                        print(" | ".join(valores))
                else:
                    print("La tabla está vacía.")
                
                print("\n")
                
    except Exception as e:
        print("\n=== ERROR DE CONEXIÓN O CONSULTA ===")
        print(e)