import os
from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

CURRENT_PATH = Path(__file__).resolve()
BASE_DIR = next(p for p in CURRENT_PATH.parents if p.name == "BackendArquitectura")
ENV_PATH = BASE_DIR / "pruebasdb" / ".env"

load_dotenv(dotenv_path=ENV_PATH, override=True)

DATABASE_URL = os.getenv("DATABASE_URL2")

if not DATABASE_URL:
    raise ValueError(f"La variable DATABASE_URL_BASE2 no fue encontrada en la ruta: {ENV_PATH}")

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

if __name__ == "__main__":
    try:
        with engine.connect() as connection:
            print(f"Conexión exitosa a la base de datos: '{engine.url.database}'")
    except Exception as e:
        print(f"Error al intentar conectar: {e}")