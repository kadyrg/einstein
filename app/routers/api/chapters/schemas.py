from pydantic import BaseModel
from fastapi import Form, Request

from app.utils import chapters_media_path_manager
from app.models import Chapter


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


class QuestionSchema(BaseModel):
    question: str

    @classmethod
    def as_form(
            cls,
            question: str = Form(...),
    ):
        return cls(question=question)
