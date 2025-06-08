from sqlalchemy.ext.asyncio import AsyncSession

from .schemas import NameSchema
from app.models import User


async def update_name(name_in: NameSchema, user: User, session: AsyncSession) -> NameSchema:
    user.first_name = name_in.first_name
    user.last_name = name_in.last_name

    await session.commit()

    return name_in
