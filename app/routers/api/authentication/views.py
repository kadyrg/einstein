from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from .schemas import EmailSchema, RegisterSchema, TokenSchema, VerifySchema, LoginSchema
from app.db import database
from . import crud


router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)


@router.post(
    path="/register",
    summary="Register",
    response_model=EmailSchema
)
async def register(
    register_in: RegisterSchema,
    session: AsyncSession = Depends(database.scoped_session_dependency)
):
    return await crud.register(register_in, session)


@router.post(
    path="/verify",
    summary="Verify",
    response_model=TokenSchema
)
async def verify(
    verify_in: VerifySchema,
    session: AsyncSession = Depends(database.scoped_session_dependency)
):
    return await crud.verify(verify_in, session)


@router.post(
    path="/login",
    summary="Login",
    response_model=TokenSchema
)
async def login(
    login_in: LoginSchema,
    session: AsyncSession = Depends(database.scoped_session_dependency)
):
    return await crud.login(login_in, session)
