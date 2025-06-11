from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, UploadFile, Request
from fastapi.responses import Response
from sqlalchemy.orm import selectinload

from .schemas import CourseSchema, CreateCourseSchema, course_schema, read_course_schema, CreateChapterSchema, \
    chapter_schema, ChapterSchema, UpdateChapterSchema
from app.models import Course, Chapter
from app.utils import course_image_manager, courses_media_path_manager, chapter_video_manager


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

    return read_course_schema(course, course.chapters, request)


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
        course_image_manager.delete(course.image_path)
        course.image_path = await course_image_manager.upload(image)

    await session.commit()

    return course_schema(course, request)


async def delete_course(course_id: int, session: AsyncSession):
    course_result = await session.execute(
        select(Course)
        .where(Course.id == course_id)
        .options(selectinload(Course.chapters))
    )

    course = course_result.scalar_one_or_none()

    if course is None:
        raise HTTPException(status_code=404, detail="Course not found")

    for chapter in course.chapters:
        chapter_video_manager.delete(chapter.video_path)

    course_image_manager.delete(course.image_path)

    await session.delete(course)
    await session.commit()

    return Response(status_code=204)


async def create_chapter(course_id: int, chapter_in: CreateChapterSchema, request, video: UploadFile, session: AsyncSession) -> ChapterSchema:
    course_result = await session.execute(
        select(Course).where(Course.id == course_id)
    )

    course = course_result.scalar_one_or_none()

    if course is None:
        raise HTTPException(status_code=404, detail="Course not found")

    video = await chapter_video_manager.upload(video)

    chapter = Chapter(
        title=chapter_in.title,
        video_path=video,
        course_id=course_id
    )

    session.add(chapter)
    await session.commit()

    return chapter_schema(chapter, request)


async def read_chapter(course_id: int, chapter_id: int, request: Request, session: AsyncSession) -> ChapterSchema:
    chapter_result = await session.execute(
        select(Chapter).where(
            Chapter.id == chapter_id,
            Chapter.course_id == course_id,
        )
    )

    chapter = chapter_result.scalar_one_or_none()

    if chapter is None:
        raise HTTPException(status_code=404, detail="Chapter not found")

    return chapter_schema(chapter, request)


async def update_chapter(course_id: int, chapter_id: int, chapter_in: UpdateChapterSchema, video: UploadFile | None, request: Request, session: AsyncSession) -> ChapterSchema:
    result = await session.execute(
        select(Chapter).where(
            Chapter.course_id == course_id,
            Chapter.id == chapter_id,
        )
    )

    chapter = result.scalar_one_or_none()

    if chapter is None:
        raise HTTPException(status_code=404, detail="Chapter not found")

    for field, value in chapter_in.model_dump().items():
        setattr(chapter, field, value)

    if video:
        chapter_video_manager.delete(chapter.video_path)
        chapter.video_path = await chapter_video_manager.upload(video)

    await session.commit()

    return chapter_schema(chapter, request)


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

    chapter_video_manager.delete(chapter.video_path)

    await session.delete(chapter)
    await session.commit()

    return Response(status_code=204)
