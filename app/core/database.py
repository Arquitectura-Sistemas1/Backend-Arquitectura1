from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config import settings


engine = create_engine(
    settings.DATABASE_URL2,
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


if __name__ == "__main__":
    try:
        with engine.connect() as connection:
            print(
                f"Conexión exitosa a la base de datos: "
                f"'{engine.url.database}'"
            )
    except Exception as e:
        print(f"Error al intentar conectar: {e}")