from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from fastapi import HTTPException

from .schemas import CreateUserSchema, GetUsersSchema, ListUsersSchema, CreateStudentSchema, StudentSchema
from app.models import User, UserType
from app.utils import password_manager


async def create_user(user_in: CreateUserSchema, session: AsyncSession) -> CreateUserSchema:
    result = await session.execute(
        select(User).where(
            User.email == user_in.email
        )
    )

    user = result.scalar_one_or_none()

    if user:
        raise HTTPException(status_code=400, detail="Email already registered")

    password = password_manager.hash_password(user_in.password)

    user = User(
        email=str(user_in.email),
        first_name=user_in.first_name,
        last_name=user_in.last_name,
        password=password,
        is_active=True,
        type=UserType.admin
    )

    session.add(user)
    await session.commit()

    return user_in


async def get_users(session: AsyncSession, page: int = 1) -> GetUsersSchema:
    limit = 10
    offset = (page - 1) * limit

    total_result = await session.execute(
        select(func.count()).select_from(User).where(User.type==UserType.student)
    )

    total = total_result.scalar_one() or 0

    result = await session.execute(
        select(User)
        .where(User.type == UserType.student)
        .order_by(-User.id)
        .offset(offset)
        .limit(limit)
    )

    users = result.scalars().all()

    pages = (total + limit - 1) // limit

    return GetUsersSchema(
        total = total,
        pages = pages,
        limit = limit,
        users = [ListUsersSchema.model_validate(user) for user in users]
    )


async def create_student(student_in: CreateStudentSchema, session: AsyncSession) -> StudentSchema:
    result = await session.execute(
        select(User).where(User.email == student_in.email)
    )

    student = result.scalar_one_or_none()

    if student:
        raise HTTPException(status_code=400, detail="Email already registered")

    student = User(
        email=str(student_in.email),
        first_name=student_in.first_name,
        last_name=student_in.last_name,
        is_active=True,
        type=UserType.student,
        password=password_manager.hash_password(student_in.password)
    )

    session.add(student)
    await session.commit()
    return StudentSchema.model_validate(student)
