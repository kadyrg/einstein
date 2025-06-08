from pydantic import BaseModel, Field, ConfigDict
from typing import Annotated
from fastapi import Form


class CreateCourseSchema(BaseModel):
    title: str = Field(max_length=50, min_length=1)

    @classmethod
    def as_form(
            cls,
            title: str = Form(...),
    ):
        return cls(title=title)


class UpdateCourseSchema(CreateCourseSchema):
    title: Annotated[str | None, Field(min_length=1, max_length=50)] = None
    image_path: str | None = None

    model_config = ConfigDict(from_attributes=True)


class ListCourseSchema(CreateCourseSchema):
    id: int


class CreateChapterSchema(CreateCourseSchema):
    pass


class ReadChapterSchema(CreateCourseSchema):
    pass


class ListChapterSchema(ReadChapterSchema):
    id: int = Field(gt=0)


class ReadCourseSchema(CreateCourseSchema):
    chapters: list[ListChapterSchema]
