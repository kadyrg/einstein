from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, Path, File, UploadFile, HTTPException
from typing import Annotated

from . import crud
from app.db import db_helper
from .schemas import CreateCourseSchema, UpdateCourseSchema, ListCourseSchema, ReadCourseSchema, CreateChapterSchema, ReadChapterSchema


router = APIRouter(
    prefix="/courses",
    tags=["Courses"],
)


@router.post(
    path="/",
    summary="Create course",
)
async def create_course(
    course_in: Annotated[CreateCourseSchema, Depends(CreateChapterSchema.as_form)],
    image: Annotated[UploadFile, File()],
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):

    return await crud.create_course(
        course_in=course_in,
        image=image,
        session=session,
    )


@router.get(
    path="/",
    summary="Get courses",
    response_model=list[ListCourseSchema]
)
async def get_courses(
    session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    return await crud.get_courses(session=session)


@router.get(
    path="/{course_id}",
    summary="Read course",
    response_model=ReadCourseSchema
)
async def read_course(
    course_id: Annotated[int, Path(gt=0)],
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.read_course(
        course_id=course_id,
        session=session,
    )


@router.patch(
    path="/{course_id}",
    summary="Update course"
)
async def update_course(
    course_id: Annotated[int, Path(gt=0)],
    course_in: UpdateCourseSchema,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.update_course(
        course_id=course_id,
        course_in=course_in,
        session=session,
    )


@router.delete(
    path="/{course_id}",
    summary="Delete course"
)
async def read_course(
    course_id: Annotated[int, Path(gt=0)],
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
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
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
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
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
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
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.delete_chapter(
        course_id=course_id,
        chapter_id=chapter_id,
        session=session,
    )
