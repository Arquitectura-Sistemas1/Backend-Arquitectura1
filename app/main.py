from fastapi import FastAPI
# Importas el router que acabamos de armar
from app.api.router import router as usuarios_router
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite cualquier origen para pruebas
    allow_credentials=True,
    allow_methods=["*"],  # Permite GET, POST, OPTIONS, etc.
    allow_headers=["*"],  # Permite Content-Type, ngrok-skip-browser-warning, etc.
)
#Registramoss el router en la aplicación
app.include_router(usuarios_router)

@app.get("/")
def read_root():
    return {"status": "ok"}
