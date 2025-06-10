import shutil
from pathlib import Path
from uuid import uuid4
from fastapi import UploadFile, HTTPException
from PIL import Image
import io

from app.core import settings
from .path import courses_media_path_manager


class ImageManager:
    media_root: Path = settings.MEDIA_ROOT
    allowed_input_formats = {"image/jpeg", "image/png", "image/webp", "image/gif"}
    output_format = "webp"

    def __init__(self):
        self.url = courses_media_path_manager.local_file_url

    async def upload(self, image: UploadFile) -> str:
        if image.content_type not in self.allowed_input_formats:
            raise HTTPException(status_code=400, detail=f"Image format is not supported")

        filename = f"{uuid4().hex}.{self.output_format}"
        image_path: Path = self.url / filename

        with open(image_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)
        return filename

course_image_manager = ImageManager()
