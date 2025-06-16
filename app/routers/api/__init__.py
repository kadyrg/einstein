from fastapi import APIRouter

from .users.views import router as users_router
from .authentication.views import router as authentication_router
from .courses.views import router as courses_router
from .chapters.views import router as chapters_router


router = APIRouter()


router.include_router(users_router)
router.include_router(authentication_router)
router.include_router(courses_router)
router.include_router(chapters_router)
