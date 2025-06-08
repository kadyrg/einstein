from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from . import crud
from app.db import db_helper
from .schemas import CreateUserSchema, MeSchema, GetUsersSchema, CreateStudentSchema, StudentSchema
from app.utils import auth_manager
from app.models import User


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post(
    path="",
    summary="Create user",
    response_model=CreateUserSchema,
)
async def create_user(
    user_in: CreateUserSchema,
    user: User = Depends(auth_manager.admin_auth),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    return await crud.create_user(user_in, session)


@router.get(
    path="",
    summary="Get users",
    response_model=GetUsersSchema,
)
async def get_users(
    page: Annotated[int, Query(ge=1, description="Page")] = 1,
    user: User = Depends(auth_manager.admin_auth),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    return await crud.get_users(session, page)


@router.post(
    path="/students",
    summary="Create student",
    response_model=StudentSchema,
)
async def create_student(
    student_in: CreateStudentSchema,
    user: User = Depends(auth_manager.admin_auth),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    return await crud.create_student(student_in, session)


@router.get(
    path="/me",
    summary="Get your data",
    response_model=MeSchema,
)
def get_me(
    user: User = Depends(auth_manager.admin_auth),
):
    return MeSchema.model_validate(user)
