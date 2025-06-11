from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from fastapi import HTTPException

from .schemas import UserSchema, CreateUserSchema, GetUsersSchema
from app.models import User, UserType
from app.utils import password_manager


async def create_admin(admin_in: CreateUserSchema, session: AsyncSession) -> UserSchema:
    result = await session.execute(
        select(User).where(
            User.email == admin_in.email
        )
    )

    admin = result.scalar_one_or_none()

    if admin:
        raise HTTPException(status_code=400, detail="Email already registered")

    password = password_manager.hash_password(admin_in.password)

    admin = User(
        email=str(admin_in.email),
        first_name=admin_in.first_name,
        last_name=admin_in.last_name,
        password=password,
        is_active=True,
        type=UserType.admin
    )

    session.add(admin)
    await session.commit()

    return UserSchema.model_validate(admin)


async def get_admins(session: AsyncSession, page: int = 1) -> GetUsersSchema:
    limit = 10
    offset = (page - 1) * limit

    total_result = await session.execute(
        select(func.count()).select_from(User).where(User.type==UserType.admin)
    )

    total = total_result.scalar_one() or 0

    result = await session.execute(
        select(User)
        .where(User.type == UserType.admin)
        .order_by(-User.id)
        .offset(offset)
        .limit(limit)
    )

    admins = result.scalars().all()

    pages = (total + limit - 1) // limit

    return GetUsersSchema(
        total = total,
        pages = pages,
        limit = limit,
        results = [UserSchema.model_validate(admin) for admin in admins]
    )


async def create_student(student_in: CreateUserSchema, session: AsyncSession) -> UserSchema:
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
    return UserSchema.model_validate(student)


async def get_students(session: AsyncSession, page: int = 1) -> GetUsersSchema:
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

    students = result.scalars().all()

    pages = (total + limit - 1) // limit

    return GetUsersSchema(
        total = total,
        pages = pages,
        limit = limit,
        results = [UserSchema.model_validate(student) for student in students]
    )


