from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from . import crud
from app.db import database
from .schemas import UserSchema, CreateUserSchema, GetUsersSchema
from app.utils import auth_manager
from app.models import User


router = APIRouter(
    prefix="/users"
)


@router.post(
    path="/admins",
    tags=["Admins"],
    summary="Create admin",
    response_model=UserSchema,
)
async def create_admin(
    admin_in: CreateUserSchema,
    session: AsyncSession = Depends(database.scoped_session_dependency)
):
    return await crud.create_admin(admin_in, session)


@router.get(
    path="/admins",
    tags=["Admins"],
    summary="Get admins",
    response_model=GetUsersSchema,
)
async def get_admins(
    page: Annotated[int, Query(ge=1, description="Page")] = 1,
    session: AsyncSession = Depends(database.scoped_session_dependency)
):
    return await crud.get_admins(session, page)


@router.post(
    path="/students",
    tags=["Students"],
    summary="Create student",
    response_model=UserSchema,
)
async def create_student(
    student_in: CreateUserSchema,
    session: AsyncSession = Depends(database.scoped_session_dependency)
):
    return await crud.create_student(student_in, session)


@router.get(
    path="/students",
    tags=["Students"],
    summary="Get students",
    response_model=GetUsersSchema,
)
async def get_admins(
    page: Annotated[int, Query(ge=1, description="Page")] = 1,
    session: AsyncSession = Depends(database.scoped_session_dependency)
):
    return await crud.get_students(session, page)


@router.get(
    path="/me",
    tags=["Users"],
    summary="Get your data",
    response_model=UserSchema,
)
def get_me(
    user: User = Depends(auth_manager.admin_auth),
):
    return UserSchema.model_validate(user)
