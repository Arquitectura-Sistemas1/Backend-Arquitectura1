# app/api/router.py
from fastapi import APIRouter
from app.api.endpoints.auth import router as auth_router
from app.api.endpoints.inventario import router as inv_router

router = APIRouter()


router.include_router(auth_router)
router.include_router(inv_router)

@router.get("/paises", tags=["Catálogos"])
def obtener_paises():
    return [
        {"id": 1, "nombre": "Guatemala"},
        {"id": 2, "nombre": "México"},
        {"id": 3, "nombre": "Estados Unidos"},
        {"id": 4, "nombre": "Canadá"},
        {"id": 5, "nombre": "España"},
    ]