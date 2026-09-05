# app/api/router.py
from fastapi import APIRouter
from app.api.endpoints.auth import router as auth_router
from app.api.endpoints.informacion import router as informacion_router
from app.api.endpoints.inventario import router as inv_router

router = APIRouter()


router.include_router(auth_router)
router.include_router(informacion_router)
router.include_router(inv_router)
