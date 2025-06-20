from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, Path, UploadFile, File, Request
from typing import Annotated

from . import crud
from app.db import database
from .schemas import QuestionSchema, ChapterSchema


router = APIRouter(
    prefix="/chapters",
    tags=["Chapters"],
)


@router.get(
    path="/{chapter_id}",
    summary="Get chapter",
    response_model=ChapterSchema
)
async def read_chapter(
    chapter_id: Annotated[int, Path(gt=0)],
    request: Request,
    # user: User = Depends(auth_manager.student_auth),
    session: AsyncSession = Depends(database.scoped_session_dependency),
):
    return await crud.read_chapter(chapter_id, request, session)



@router.post(
    path="/{chapter_id}/ask",
    summary="Ask question",
)
async def ask_question(
    chapter_id: Annotated[int, Path(gt=0)],
    image: Annotated[UploadFile, File(...)],
    question_in: Annotated[QuestionSchema, Depends(QuestionSchema.as_form)],
    # user: user: User = Depends(auth_manager.student_auth),
    session: AsyncSession = Depends(database.scoped_session_dependency),
):
    return await crud.ask_question(chapter_id, image, question_in, session)
