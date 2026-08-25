import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.engine import make_url
from sqlalchemy.orm import sessionmaker

load_dotenv()

DATABASE_URL2 = os.getenv("DATABASE_URL2")

url_obj = make_url(DATABASE_URL2)
nombre_db = url_obj.database

engine = create_engine(DATABASE_URL2, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def actualizar_valores_directo():
    print(f"Conectando a '{nombre_db}'...\n")
    
    # Solicitar el valor exacto que se insertará
    valor_directo = input("Ingresa el texto exacto a colocar en HashContrasena: ").strip()
    
    if not valor_directo:
        print("Error: El texto no puede estar vacío.")
        return
    
    tablas_a_actualizar = ["CredencialEmpleado", "CredencialUsuario"]
    
    session = SessionLocal()
    try:
        for tabla in tablas_a_actualizar:
            print(f"==========================================")
            print(f"ACTUALIZANDO TABLA: {tabla}")
            print(f"==========================================")
            
            # Asignación directa del texto ingresado
            query_update = text(f"""
                UPDATE {tabla}
                SET HashContrasena = :valor
            """)
            resultado = session.execute(query_update, {"valor": valor_directo})
            session.commit()
            
            print(f"Registros actualizados: {resultado.rowcount}\n")
            
            # Verificación de datos guardados
            query_select = text(f"SELECT TOP 5 * FROM {tabla}")
            registros = session.execute(query_select).mappings().all()
            
            if registros:
                columnas = list(registros[0].keys())
                print(" | ".join(columnas))
                print("-" * 50)
                for reg in registros:
                    print(" | ".join(str(reg[col]) for col in columnas))
            print("\n")
            
        print("¡Proceso finalizado con éxito!")
        
    except Exception as e:
        session.rollback()
        print("\n=== ERROR DURANTE LA ACTUALIZACIÓN ===")
        print(e)
    finally:
        session.close()

if __name__ == "__main__":
    actualizar_valores_directo()