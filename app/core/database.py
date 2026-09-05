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

def ejecutar_sp_commit(db: Session, nombre_procedimiento: str, **parametros: Any):
    try:
        lista_parametros = ", ".join(f"@{key} = :{key}" for key in parametros)
        sql = text(f"EXEC dbo.{nombre_procedimiento} {lista_parametros}")
        
        resultado = db.execute(sql, parametros)
        
        datos = [dict(row) for row in resultado.mappings().all()] if resultado.returns_rows else []
        db.commit()
        return datos
    except Exception as e:
        db.rollback()
        raise e