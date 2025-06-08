from fastapi import APIRouter

from .courses.views import router as courses_router
from .auth.views import router as auth_router
from .users.views import router as users_router


router = APIRouter()


router.include_router(auth_router)
router.include_router(users_router)
router.include_router(courses_router)
