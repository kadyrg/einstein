from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
import uvicorn
from contextlib import asynccontextmanager

from db import db_helper
from models import Base
from api import router as api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(
    lifespan=lifespan,
    title="Einstein",
    version="1.0.0",
    description="Einstein online AI tutor"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(api_router)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True)
