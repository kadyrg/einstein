from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from .schemas import MeSchema, NameSchema
from models import User
from auth import auth_manager
from . import crud
from db import db_helper


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.get(
    path="/me",
    name="Your personal data",
    description="Get your personal deta on Einstein platform",
    response_model=MeSchema
)
def get_me(
    user: User = Depends(auth_manager.student_auth)
):
    return MeSchema.model_validate(user)


@router.put(
    path="/me/name",
    name="Update your name",
    description="Update your first and last name",
    response_model=NameSchema
)
async def update_name(
    name_in: NameSchema,
    user: User = Depends(auth_manager.student_auth),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    return await crud.update_name(name_in, user, session)
