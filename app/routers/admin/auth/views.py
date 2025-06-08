from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import db_helper
from . import crud
from .schemas import LoginSchema, TokenSchema


router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)


@router.post(
    path="/login",
    summary="Login",
    response_model=TokenSchema,
)
async def login(
    login_in: LoginSchema,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    return await crud.login(login_in, session)
