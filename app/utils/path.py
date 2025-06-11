from pathlib import Path

from fastapi import Request
from app.core import settings


class MediaPathManager:
    root_path = settings.MEDIA_ROOT

    def __init__(self, folder: str):
        self.folder=folder

    @property
    def local_file_url(self) -> Path:
        return Path(self.root_path, self.folder)

    def local_file_path(self, filename: str) -> Path:
        return self.root_path / self.folder / filename

    def file_path(self, request: Request, filename: str) -> str:
        return f"{request.base_url}media/{self.folder}/{filename}"

courses_media_path_manager = MediaPathManager("courses")

chapters_media_path_manager = MediaPathManager("chapters")
