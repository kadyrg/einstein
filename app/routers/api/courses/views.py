from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, Path, Request, UploadFile, File
from typing import Annotated

from . import crud
from app.db import database
from .schemas import CourseSchema, ReadCourseSchema,  ChapterSchema
from app.models import User
from app.utils import auth_manager


router = APIRouter(
    prefix="/courses",
    tags=["Courses"],
)


@router.get(
    path="",
    summary="Get courses",
    response_model=list[CourseSchema]
)
async def get_courses(
    request: Request,
    # user: User = Depends(auth_manager.student_auth),
    session: AsyncSession = Depends(database.scoped_session_dependency)
):
    return await crud.get_courses(request, session)


@router.get(
    path="/{course_id}",
    summary="Read course",
    response_model=ReadCourseSchema
)
async def read_course(
    course_id: Annotated[int, Path(gt=0)],
    request: Request,
    # user: User = Depends(auth_manager.student_auth),
    session: AsyncSession = Depends(database.scoped_session_dependency),
):
    return await crud.read_course(course_id, request, session)


@router.get(
    path="/{course_id}/chapters/{chapter_id}",
    summary="Get chapter",
    response_model=ChapterSchema
)
async def read_chapter(
    course_id: Annotated[int, Path(gt=0)],
    chapter_id: Annotated[int, Path(gt=0)],
    request: Request,
    # user: User = Depends(auth_manager.student_auth),
    session: AsyncSession = Depends(database.scoped_session_dependency),
):
    return await crud.read_chapter(course_id, chapter_id, request, session)
