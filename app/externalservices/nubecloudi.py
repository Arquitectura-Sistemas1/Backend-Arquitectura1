import io
import cloudinary
import cloudinary.uploader
from cloudinary.utils import cloudinary_url
from fastapi import UploadFile
from app.config import settings


name = settings.CLOUDNANE
key = settings.CLOUDKEY
secret = settings.CLOUDSECRET

cloudinary.config(
    cloud_name=name,
    api_key=key,
    api_secret=secret,
    secure=True
)


def subir_imagen(file: UploadFile) -> str:
    upload_result = cloudinary.uploader.upload(file.file)
    return upload_result["secure_url"]


def subir_factura_imagen(numero_factura: str, contenido_png: bytes) -> str:
    """
    Sube los bytes de la imagen PNG de la factura a Cloudinary exactamente igual que subir_imagen.
    """
    file_obj = io.BytesIO(contenido_png)
    file_obj.name = f"{numero_factura}.png"

    upload_result = cloudinary.uploader.upload(file_obj)
    return upload_result["secure_url"]
