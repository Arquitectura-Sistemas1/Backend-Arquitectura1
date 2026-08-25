from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from typing import Any
from sqlalchemy import text
from app.config import settings


engine = create_engine(
    settings.DATABASE_URL2,
    pool_pre_ping=True,
    future=True,
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=Session,
)


def ejecutar_sp(db: Session, nombre_procedimiento: str, **parametros: Any):

    lista_parametros = ", ".join(f"@{key} = :{key}" for key in parametros)
    sql = text(f"EXEC dbo.{nombre_procedimiento} {lista_parametros}")
    resultado = db.execute(sql, parametros)
    return resultado.mappings().all()


if __name__ == "__main__":
    try:
        with engine.connect() as connection:
            print(
                f"Conexión exitosa a la base de datos: "
                f"'{engine.url.database}'"
            )
    except Exception as e:
        print(f"Error al intentar conectar: {e}")

