from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, Request, UploadFile
from sqlalchemy.orm import selectinload

from .schemas import CourseSchema, course_schema, read_course_schema, chapter_schema, ChapterSchema
from app.models import Course, Chapter


async def get_courses(request: Request, session: AsyncSession) -> list[CourseSchema]:
    result = await session.execute(
        select(Course).order_by(-Course.id)
    )
    courses = result.scalars().all()
    return [course_schema(course, request) for course in courses]


async def read_course(course_id: int, request: Request, session: AsyncSession) -> CourseSchema:
    result = await session.execute(
        select(Course)
        .where(Course.id == course_id)
        .options(selectinload(Course.chapters))
    )
    course = result.scalar_one_or_none()
    if course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    return read_course_schema(course, course.chapters, request)


