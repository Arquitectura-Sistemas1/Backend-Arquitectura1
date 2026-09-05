from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

#  iniciar el limtador en ip cliente
limiter = Limiter(key_func=get_remote_address)

app = FastAPI()

# egistrandolo en la app
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://luxury-roster-uncouth.ngrok-free.dev"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# importar y registrar el router
from app.api.router import router as usuarios_router
app.include_router(usuarios_router)

@app.get("/")
def read_root():
    return {"status": "ok"}