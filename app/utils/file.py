import os
import shutil
from pathlib import Path
from typing import Iterable
from uuid import uuid4
from fastapi import UploadFile, HTTPException

from app.core import settings
from .path import courses_media_path_manager, chapters_media_path_manager


class FileManager:
    media_root: Path = settings.MEDIA_ROOT

    def __init__(self, allowed_input_formats: Iterable[str], output_format: str, url: Path):
        self.allowed_input_formats = allowed_input_formats
        self.output_format = output_format
        self.url = url

    async def upload(self, file: UploadFile) -> str:
        if file.content_type not in self.allowed_input_formats:
            raise HTTPException(status_code=400, detail="Format not supported")

        filename = f"{uuid4().hex}.{self.output_format}"
        image_path: Path = self.url / filename

        with open(image_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        return filename

    def delete(self, filename: str):
        file_path = self.url / filename
        if file_path.exists():
            try:
                os.remove(file_path)
            except OSError as e:
                raise HTTPException(status_code=404, detail=f"File cannot be deleted: {e}")


course_image_manager = FileManager(
    allowed_input_formats = {"image/jpeg", "image/png", "image/webp", "image/gif"},
    output_format = "webp",
    url = courses_media_path_manager.local_file_url
)

chapter_video_manager = FileManager(
    allowed_input_formats={
        "video/mp4",
        "video/quicktime",
        "video/x-msvideo",
        "video/webm",
        "video/x-matroska",
        "video/3gpp",
        "video/3gpp2",
        "video/mpeg",
        "video/ogg",
    },
    output_format = "mp4",
    url = chapters_media_path_manager.local_file_url
)
