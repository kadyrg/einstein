from fastapi import APIRouter

from .users.views import router as users_router
from .authentication.views import router as authentication_router


router = APIRouter(
    prefix="/api"
)


router.include_router(users_router)
router.include_router(authentication_router)
