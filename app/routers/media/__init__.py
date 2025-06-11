from fastapi import APIRouter

from .courses.views import router as courses_router
from .chapters.views import router as chapters_router


router = APIRouter()


router.include_router(courses_router)
router.include_router(chapters_router)
