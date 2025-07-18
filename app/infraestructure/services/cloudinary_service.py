import cloudinary
import cloudinary.uploader
import cloudinary.api
from typing import Optional
import os
from dotenv import load_dotenv

load_dotenv()

class CloudinaryService:
    def __init__(self):
        cloudinary.config(
            cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
            api_key=os.getenv("CLOUDINARY_API_KEY"),
            api_secret=os.getenv("CLOUDINARY_API_SECRET")
        )
    
    def upload_image(self, image_bytes: bytes, public_id: str) -> str:
        """Sube una imagen a Cloudinary y retorna la URL"""
        try:
            result = cloudinary.uploader.upload(
                image_bytes,
                public_id=public_id,
                folder="productos",
                resource_type="image"
            )
            return result.get("secure_url")
        except Exception as e:
            raise Exception(f"Error al subir imagen a Cloudinary: {str(e)}")
    
    def delete_image(self, public_id: str) -> bool:
        """Elimina una imagen de Cloudinary"""
        try:
            result = cloudinary.uploader.destroy(f"productos/{public_id}")
            return result.get("result") == "ok"
        except Exception as e:
            print(f"Error al eliminar imagen de Cloudinary: {str(e)}")
            return False