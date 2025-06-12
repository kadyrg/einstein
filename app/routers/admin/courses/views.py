from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, Path, File, UploadFile, Request, Form
from typing import Annotated

from . import crud
from app.db import database
from .schemas import CourseSchema, ReadCourseSchema, CreateCourseSchema, CreateChapterSchema, ChapterSchema, UpdateChapterSchema
from app.models import User
from app.utils import auth_manager


router = APIRouter(
    prefix="/courses",
    tags=["Courses"],
)


@router.post(
    path="/",
    summary="Create course",
    response_model=CourseSchema,
)
async def create_course(
    course_in: Annotated[CreateCourseSchema, Depends(CreateCourseSchema.as_form)],
    image: Annotated[UploadFile, File(...)],
    request: Request,
    # user: User = Depends(auth_manager.admin_auth),
    session: AsyncSession = Depends(database.scoped_session_dependency),
):
    return await crud.create_course(course_in, image, request, session)


@router.get(
    path="/",
    summary="Get courses",
    response_model=list[CourseSchema]
)
async def get_courses(
    request: Request,
    # user: User = Depends(auth_manager.admin_auth),
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
    # user: User = Depends(auth_manager.admin_auth),
    session: AsyncSession = Depends(database.scoped_session_dependency),
):
    return await crud.read_course(course_id, request, session)


@router.patch(
    path="/{course_id}",
    summary="Update course",
    response_model=CourseSchema
)
async def update_course(
    course_id: Annotated[int, Path(gt=0)],
    request: Request,
    image: Annotated[UploadFile | None, File()] = None,
    course_title: Annotated[str | None, Form(min_length=1, max_length=50)] = None,
    # user: User = Depends(auth_manager.admin_auth),
    session: AsyncSession = Depends(database.scoped_session_dependency)
):
    return await crud.update_course(course_id, course_title, image, request, session)


@router.delete(
    path="/{course_id}",
    summary="Delete course"
)
async def delete_course(
    course_id: Annotated[int, Path(gt=0)],
    # user: User = Depends(auth_manager.admin_auth),
    session: AsyncSession = Depends(database.scoped_session_dependency),
):
    return await crud.delete_course(course_id, session)


@router.post(
    path="/{course_id}/chapters",
    summary="Create chapter",
    response_model=ChapterSchema,
)
async def create_chapter(
    course_id: Annotated[int, Path(gt=0)],
    chapter_in: Annotated[CreateChapterSchema, Depends(CreateChapterSchema.as_form)],
    request: Request,
    video: Annotated[UploadFile, File(...)],
    # user: User = Depends(auth_manager.admin_auth),
    session: AsyncSession = Depends(database.scoped_session_dependency),
):
    return await crud.create_chapter(course_id, chapter_in, request, video, session)


@router.get(
    path="/{course_id}/chapters/{chapter_id}",
    summary="Get chapter",
    response_model=ChapterSchema
)
async def read_chapter(
    course_id: Annotated[int, Path(gt=0)],
    chapter_id: Annotated[int, Path(gt=0)],
    request: Request,
    # user: User = Depends(auth_manager.admin_auth),
    session: AsyncSession = Depends(database.scoped_session_dependency),
):
    return await crud.read_chapter(course_id, chapter_id, request, session)


@router.patch(
    path="/{course_id}/chapters/{chapter_id}",
    summary="Update chapter",
    response_model=ChapterSchema
)
async def update_chapter(
    course_id: Annotated[int, Path(gt=0)],
    chapter_id: Annotated[int, Path(gt=0)],
    chapter_in: Annotated[UpdateChapterSchema, Depends(UpdateChapterSchema.as_form)],
    request: Request,
    video: Annotated[UploadFile | None, File()] = None,
    # user: User = Depends(auth_manager.admin_auth),
    session: AsyncSession = Depends(database.scoped_session_dependency),
):
    return await crud.update_chapter(course_id, chapter_id, chapter_in, video, request, session)


@router.delete(
    path="/{course_id}/chapters/{chapter_id}",
    summary="Delete chapter"
)
async def read_chapter(
    course_id: Annotated[int, Path(gt=0)],
    chapter_id: Annotated[int, Path(gt=0)],
    # user: User = Depends(auth_manager.admin_auth),
    session: AsyncSession = Depends(database.scoped_session_dependency),
):
    return await crud.delete_chapter(course_id, chapter_id, session)
