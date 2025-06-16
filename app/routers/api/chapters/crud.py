from sqlalchemy import select
from sqlalchemy.orm import selectinload
from fastapi import UploadFile, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession

from .schemas import QuestionSchema, chapter_schema, ChapterSchema
from app.models import Chapter
from app.core.dependencies import ask_ai


async def read_chapter(chapter_id: int, request: Request, session: AsyncSession) -> ChapterSchema:
    chapter_result = await session.execute(
        select(Chapter).where(
            Chapter.id == chapter_id
        )
    )
    chapter = chapter_result.scalar_one_or_none()
    if chapter is None:
        raise HTTPException(status_code=404, detail="Chapter not found")
    return chapter_schema(chapter, request)


async def ask_question(chapter_id: int, image: UploadFile, question_in: QuestionSchema, session: AsyncSession):
    result = await session.execute(
        select(Chapter)
        .options(selectinload(Chapter.course))
        .where(
            Chapter.id == chapter_id
        )
    )

    chapter = result.scalar_one_or_none()

    if chapter is None:
        raise HTTPException(status_code=404, detail="Chapter not found")

    course_name = chapter.course.title
    chapter_name = chapter.title
    question = question_in.question
    image = image
    return await ask_ai.ask_question(course_name, chapter_name, question, image)