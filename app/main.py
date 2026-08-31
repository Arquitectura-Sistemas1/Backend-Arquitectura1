from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr

from app.externalservices.msjresend import enviar_correo

app = FastAPI()


class EnviarCodigoRequest(BaseModel):
    nombre: str
    correo: EmailStr
    code: str
    tipo: str = "registro"


@app.post("/enviar-codigo")
def enviar_codigo(datos: EnviarCodigoRequest):
    try:
        resultado = enviar_correo(
            nombre_original=datos.nombre,
            correo_destino=datos.correo,
            code=datos.code,
            tipo=datos.tipo,
        )
        return {"status": "ok", "resultado": resultado}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))