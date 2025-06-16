from fastapi import Request
from pydantic import BaseModel

from app.utils import courses_media_path_manager
from app.models import Course, Chapter
from app.routers.api.chapters.schemas import ChapterSchema, chapter_schema


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
