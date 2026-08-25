from fastapi import FastAPI
# Importas el router que acabamos de armar
from app.api.router import router as usuarios_router

app = FastAPI()

# Registras el router en la aplicación
app.include_router(usuarios_router)

@app.get("/")
def read_root():
    return {"status": "ok"}
