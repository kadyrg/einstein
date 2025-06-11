from fastapi.responses import FileResponse
from fastapi import APIRouter, HTTPException

from app.core import settings


router = APIRouter(
    prefix="/chapters",
    tags=["Chapters"]
)


@router.get(
    path="/{video_path}",
    summary="Get course image",
)
async def get_course_image(
    video_path: str
) -> FileResponse:
    path = settings.MEDIA_ROOT / "chapters" / video_path
    if not path.exists():
        raise HTTPException(status_code=404, detail="Video not found")
    return FileResponse(path)
