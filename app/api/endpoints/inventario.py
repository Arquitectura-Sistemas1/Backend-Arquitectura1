
from fastapi import APIRouter, Depends, status, Request  # <-- 1. Importa Request
from app.core.database import Session
from app.api.deps import get_db
 #falta completarla con importacion de las funciones en app.services.inventario
from datetime import date

router = APIRouter(prefix="/inv", tags=["Inventario"])
