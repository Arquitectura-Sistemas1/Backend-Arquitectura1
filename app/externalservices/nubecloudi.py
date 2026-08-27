import cloudinary
import cloudinary.uploader

from app.config import settings


# Configuración de Cloudinary
cloudinary.config(
    cloud_name=settings.CLOUDINARY_CLOUD_NAME,
    api_key=settings.CLOUDINARY_API_KEY,
    api_secret=settings.CLOUDINARY_API_SECRET,
    secure=True
)


def subir_imagen(archivo):
    """
    Sube una imagen a Cloudinary.
    Retorna la URL segura y el public_id de la imagen.
    """

    resultado = cloudinary.uploader.upload(
        archivo,
        folder="videojuegos"
    )

    return {
        "url": resultado["secure_url"],
        "public_id": resultado["public_id"]
    }


def eliminar_imagen(public_id: str):
    """
    Elimina una imagen de Cloudinary utilizando su public_id.
    """

    resultado = cloudinary.uploader.destroy(public_id)

    return resultado