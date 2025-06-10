from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, UploadFile, Request
from fastapi.responses import Response
from sqlalchemy.orm import selectinload
import os

from .schemas import CourseSchema, CreateCourseSchema, course_schema, CreateChapterSchema, ReadChapterSchema
from app.models import Course, Chapter
from app.utils import course_image_manager, courses_media_path_manager


async def create_course(course_in: CreateCourseSchema, image: UploadFile, request: Request, session: AsyncSession) -> CourseSchema:
    course_result = await session.execute(
        select(Course).where(
            Course.title == course_in.title,
        )
    )

    course = course_result.scalar_one_or_none()

    if course:
        raise HTTPException(status_code=400, detail="Course already exists")

    image_path = await course_image_manager.upload(image)

    course = Course(
        title=course_in.title,
        image_path=image_path,
    )

    session.add(course)
    await session.commit()

    return course_schema(course, request)


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

    return course_schema(course, request)


async def update_course(course_id: int, course_title: str, image: UploadFile | None, request: Request, session: AsyncSession) -> CourseSchema:
    course_result = await session.execute(
        select(Course).where(Course.id == course_id)
    )

    course = course_result.scalar_one_or_none()

    if course is None:
        raise HTTPException(status_code=404, detail="Course not found")

    if course_title:
        course.title = course_title

    if image:
        old_image = course.image_path
        old_image_path = courses_media_path_manager.local_file_path(old_image)
        if old_image_path.exists():
            os.remove(old_image_path)
        image = await course_image_manager.upload(image)
        course.image_path = image

    await session.commit()

    return course_schema(course, request)


async def delete_course(course_id: int, session: AsyncSession):
    course_result = await session.execute(
        select(Course).where(Course.id == course_id)
    )

    course = course_result.scalar_one_or_none()

    if course is None:
        raise HTTPException(status_code=404, detail="Course not found")

    image_path = courses_media_path_manager.local_file_path(course.image_path)
    if image_path.exists():
        os.remove(image_path)
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
