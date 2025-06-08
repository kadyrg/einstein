from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException

from .schemas import LoginSchema, TokenSchema
from app.models import User, UserType
from app.utils import password_manager, auth_manager


async def login(login_in: LoginSchema, session: AsyncSession) -> TokenSchema:
    result = await session.execute(
        select(User).where(
            User.email == login_in.email,
            User.type == UserType.admin
        )
    )

    user = result.scalar_one_or_none()

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    password = password_manager.verify_password(login_in.password, user.password)

    if not password:
        raise HTTPException(status_code=400, detail="Invalid password")

    token = auth_manager.generate_token(user.id)

    return TokenSchema(
        token=token
    )
