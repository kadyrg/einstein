from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, Path, File, UploadFile, Request, Form
from typing import Annotated

from . import crud
from app.db import database
from .schemas import CourseSchema, CreateCourseSchema, CreateChapterSchema, ReadChapterSchema


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
    session: AsyncSession = Depends(database.scoped_session_dependency)
):
    return await crud.get_courses(request, session)


@router.get(
    path="/{course_id}",
    summary="Read course",
    response_model=CourseSchema
)
async def read_course(
    course_id: Annotated[int, Path(gt=0)],
    request: Request,
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

    session: AsyncSession = Depends(database.scoped_session_dependency)
):
    return await crud.update_course(course_id, course_title, image, request, session)


@router.delete(
    path="/{course_id}",
    summary="Delete course"
)
async def read_course(
    course_id: Annotated[int, Path(gt=0)],
    session: AsyncSession = Depends(database.scoped_session_dependency),
):
    return await crud.delete_course(
        course_id=course_id,
        session=session,
    )


@router.post(
    path="/{course_id}/chapters",
    summary="Create chapter",
    response_model=CreateChapterSchema,
)
async def create_chapter(
    course_id: Annotated[int, Path(gt=0)],
    chapter_in: CreateChapterSchema,
    session: AsyncSession = Depends(database.scoped_session_dependency),
):
    return await crud.create_chapter(
        course_id=course_id,
        chapter_in=chapter_in,
        session=session,
    )


@router.get(
    path="/{course_id}/chapters/{chapter_id}",
    summary="Get chapter",
    response_model=ReadChapterSchema
)
async def read_chapter(
    course_id: Annotated[int, Path(gt=0)],
    chapter_id: Annotated[int, Path(gt=0)],
    session: AsyncSession = Depends(database.scoped_session_dependency),
):
    return await crud.read_chapter(
        course_id=course_id,
        chapter_id=chapter_id,
        session=session,
    )


@router.delete(
    path="/{course_id}/chapters/{chapter_id}",
    summary="Depete chapter"
)
async def read_chapter(
    course_id: Annotated[int, Path(gt=0)],
    chapter_id: Annotated[int, Path(gt=0)],
    session: AsyncSession = Depends(database.scoped_session_dependency),
):
    return await crud.delete_chapter(
        course_id=course_id,
        chapter_id=chapter_id,
        session=session,
    )
