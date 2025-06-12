from fastapi import Request
from pydantic import BaseModel, Field
from fastapi import Form

from app.utils import courses_media_path_manager, chapters_media_path_manager
from app.models import Course, Chapter


class CreateCourseSchema(BaseModel):
    title: str = Field(max_length=50, min_length=1)

    @classmethod
    def as_form(
            cls,
            title: str = Form(...),
    ):
        return cls(title=title)


class CourseSchema(BaseModel):
    id: int
    title: str
    image: str

def course_schema(course: Course, request: Request) -> CourseSchema:
    image = courses_media_path_manager.file_path(request, course.image_path)

    return CourseSchema(
        id=course.id,
        title=course.title,
        image=image
    )


class UpdateCourseSchema(BaseModel):
    title: str | None = Field(default=None, max_length=50, min_length=1)

    @classmethod
    def as_form(
            cls,
            title: str = Form(None),
    ):
        return cls(title=title)


class CreateChapterSchema(BaseModel):
    title: str = Field(max_length=50, min_length=1)

    @classmethod
    def as_form(
            cls,
            title: str = Form(...),
    ):
        return cls(title=title)


class ChapterSchema(BaseModel):
    id: int
    title: str
    video: str

def chapter_schema(chapter: Chapter, request: Request) -> ChapterSchema:
    video = chapters_media_path_manager.file_path(request, chapter.video_path)

    return ChapterSchema(
        id=chapter.id,
        title=chapter.title,
        video=video
    )


class UpdateChapterSchema(BaseModel):
    title: str | None = Field(default=None, max_length=50, min_length=1)

    @classmethod
    def as_form(
            cls,
            title: str = Form(None),
    ):
        return cls(title=title)


class ReadCourseSchema(CourseSchema):
    chapters: list[ChapterSchema]

def read_course_schema(course: Course, chapters: list[Chapter], request: Request):
    image = courses_media_path_manager.file_path(request, course.image_path)

    return ReadCourseSchema(
        id=course.id,
        title=course.title,
        image=image,
        chapters=[chapter_schema(chapter, request) for chapter in chapters],
    )
