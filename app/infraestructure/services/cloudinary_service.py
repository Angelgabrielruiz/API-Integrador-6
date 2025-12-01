import cloudinary
import cloudinary.uploader
import cloudinary.api
from typing import Optional
import os
from dotenv import load_dotenv
import time
import random

load_dotenv()

class CloudinaryService:
    def __init__(self):
        cloudinary.config(
            cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
            api_key=os.getenv("CLOUDINARY_API_KEY"),
            api_secret=os.getenv("CLOUDINARY_API_SECRET")
        )
    
    def upload_image(self, image_bytes: bytes, public_id: str) -> str:
        max_retries = 3
        base_delay = 0.5
        attempt = 0
        while True:
            try:
                result = cloudinary.uploader.upload(
                    image_bytes,
                    public_id=public_id,
                    folder="productos",
                    resource_type="image"
                )
                url = result.get("secure_url")
                if not url:
                    raise Exception("Respuesta sin URL")
                return url
            except Exception as e:
                attempt += 1
                if attempt > max_retries:
                    raise Exception(f"Error al subir imagen a Cloudinary: {str(e)}")
                delay = base_delay * (2 ** (attempt - 1))
                delay = delay + random.uniform(0, delay / 2)
                time.sleep(delay)
    
    def delete_image(self, public_id: str) -> bool:
        max_retries = 3
        base_delay = 0.5
        attempt = 0
        while True:
            try:
                result = cloudinary.uploader.destroy(f"productos/{public_id}")
                return result.get("result") == "ok"
            except Exception as e:
                attempt += 1
                if attempt > max_retries:
                    return False
                delay = base_delay * (2 ** (attempt - 1))
                delay = delay + random.uniform(0, delay / 2)
                time.sleep(delay)
