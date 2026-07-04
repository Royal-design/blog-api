from cloudinary import uploader
import cloudinary
from fastapi import UploadFile
from httpx import delete
from app.core.config import settings
from app.core.exceptions import AppException

class CloudinaryService:
    def __init__(self):
        cloudinary.config(
            cloud_name=settings.cloudinary_cloud_name,
            api_key=settings.cloudinary_api_key,
            api_secret=settings.cloudinary_api_secret,
            secure=True,
        )
    def upload_image(self, image:UploadFile, folder:str = "blog")->dict:
        if not image.content_type.startswith("image/"):
            raise AppException(
                status_code=400,
                detail="Invalid file type. Only image files are allowed.",
            )
        result = uploader.upload(
            image.file,
            folder=folder,
            public_id=image.filename.rsplit(".", 1)[0],
            use_filename=True,
            unique_filename=True,
            overwrite=False,
            resource_type="image",
        )
        return {
            "url": result["secure_url"],
            "public_id": result["public_id"],
        }
    
    def delete_image(self, public_id:str)->None:
        if not public_id:
            raise AppException(
                status_code=400,
                detail="public id is required",
            )
        uploader.destroy(public_id, resource_type="image")