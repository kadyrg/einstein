from fastapi import FastAPI

from .api import router as api_router
from .admin import router as admin_router
from .media import router as media_router


api_description = """
    Einstein API
"""

api = FastAPI(
    title="Einstein API",
    version="1.0.0",
    description=api_description
)


admin_description = """
    Einstein Admin
"""

admin = FastAPI(
    title="Einstein Admin",
    version="1.0.0",
    description=admin_description
)


media_description = """
    Einstein Media Filesystem
"""


media = FastAPI(
    title="Einstein Media",
    version="1.0.0",
    description=media_description
)


api.include_router(api_router)
admin.include_router(admin_router)
media.include_router(media_router)
