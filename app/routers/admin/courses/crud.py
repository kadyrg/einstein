from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, UploadFile
from fastapi.responses import Response
from sqlalchemy.orm import selectinload
from uuid import uuid4

from .schemas import CreateCourseSchema, ListCourseSchema, ReadCourseSchema, CreateChapterSchema, ReadChapterSchema, \
    UpdateCourseSchema
from app.models import Course, Chapter
from app.utils import course_image_manager


async def create_course(course_in: CreateCourseSchema, image: UploadFile, session: AsyncSession) -> CreateCourseSchema:
    course_result = await session.execute(
        select(Course).where(
            Course.title == course_in.title,
        )
    )

    course = course_result.scalar_one_or_none()

    if course:
        raise HTTPException(status_code=400, detail="Course already exists")

    image_path = await course_image_manager.upload_file(image, "courses")

    course = Course(**course_in.model_dump(), image_path=image_path)

    session.add(course)

    await session.commit()

    return course_in


async def get_courses(session: AsyncSession) -> list[ListCourseSchema]:
    result = await session.execute(
        select(Course).order_by(-Course.id)
    )

    courses = result.scalars().all()

    return [ListCourseSchema.model_validate(course) for course in courses]


async def read_course(course_id: int, session: AsyncSession) -> ReadCourseSchema:
    result = await session.execute(
        select(Course)
        .options(selectinload(Course.chapters))
        .where(Course.id == course_id)
    )

    course = result.scalar_one_or_none()

    if course is None:
        raise HTTPException(status_code=404, detail="Course not found")

    image = course_image_manager.get_image(course.image_path).bod

    return ReadCourseSchema.model_validate(course)


async def update_course(course_id: int, course_in: UpdateCourseSchema, session: AsyncSession):
    course_result = await session.execute(
        select(Course).where(Course.id == course_id)
    )

    course = course_result.scalar_one_or_none()

    if course is None:
        raise HTTPException(status_code=404, detail="Course not found")

    for field, value in course_in.model_dump(exclude_unset=True).items():
        setattr(course, field, value)

    await session.commit()

    return course


async def delete_course(course_id: int, session: AsyncSession):
    course_result = await session.execute(
        select(Course).where(Course.id == course_id)
    )

    course = course_result.scalar_one_or_none()

    if course is None:
        raise HTTPException(status_code=404, detail="Course not found")

    await session.delete(course)
    await session.commit()

    return Response(status_code=204)


async def create_chapter(course_id: int, chapter_in: CreateChapterSchema, session: AsyncSession) -> CreateChapterSchema:
    course_result = await session.execute(
        select(Course).where(Course.id == course_id)
    )

    course = course_result.scalar_one_or_none()

    if course is None:
        raise HTTPException(status_code=404, detail="Course not found")

    chapter = Chapter(course_id=course_id, **chapter_in.model_dump())

    session.add(chapter)

    await session.commit()

    return chapter_in


async def read_chapter(course_id: int, chapter_id: int, session: AsyncSession) -> ReadChapterSchema:

    chapter_result = await session.execute(
        select(Chapter).where(
            Chapter.id == chapter_id,
            Chapter.course_id == course_id,
        )
    )

    chapter = chapter_result.scalar_one_or_none()

    if chapter is None:
        raise HTTPException(status_code=404, detail="Chapter not found")

    return ReadChapterSchema.model_validate(chapter)


async def delete_chapter(course_id: int, chapter_id: int, session: AsyncSession):
    chapter_result = await session.execute(
        select(Chapter).where(
            Chapter.id == chapter_id,
            Chapter.course_id == course_id,
        )
    )

    chapter = chapter_result.scalar_one_or_none()

    if chapter is None:
        raise HTTPException(status_code=404, detail="Chapter not found")

    await session.delete(chapter)
    await session.commit()

    return Response(status_code=204)
