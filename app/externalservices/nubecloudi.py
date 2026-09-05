import cloudinary
import cloudinary.uploader
from cloudinary.utils import cloudinary_url
from fastapi import UploadFile
from app.config import settings


name = settings.CLOUDNANE
key = settings.CLOUDKEY
secret = settings.CLOUDSECRET

cloudinary.config( 
    cloud_name = name, 
    api_key = key, 
    api_secret = secret, # Click 'View API Keys' above to copy your API secret
    secure=True
    )

def subir_imagen(file: UploadFile) -> str:
    upload_result = cloudinary.uploader.upload(file.file)
    return upload_result["secure_url"]
