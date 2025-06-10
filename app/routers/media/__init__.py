from fastapi import APIRouter

from .courses.views import router as courses_router


router = APIRouter()


router.include_router(courses_router)
