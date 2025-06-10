from fastapi import Request

from pydantic import BaseModel, Field
from fastapi import Form
from app.utils import courses_media_path_manager
from app.models import Course


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



class CreateChapterSchema(CreateCourseSchema):
    pass


class ReadChapterSchema(CreateCourseSchema):
    pass


class ListChapterSchema(ReadChapterSchema):
    id: int = Field(gt=0)


class ReadCourseSchema(CreateCourseSchema):
    chapters: list[ListChapterSchema]
