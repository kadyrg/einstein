from fastapi.responses import FileResponse
from fastapi import APIRouter, HTTPException

from app.core import settings


router = APIRouter(
    prefix="/courses",
    tags=["Courses"]
)


@router.get(
    path="/{image_path}",
    summary="Get course image",
)
async def get_course_image(
    image_path: str
) -> FileResponse:
    path = settings.MEDIA_ROOT / "courses" / image_path
    if not path.exists():
        raise HTTPException(status_code=404, detail="Image not found")
    return FileResponse(path)
