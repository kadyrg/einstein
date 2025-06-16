from pydantic import BaseModel
from fastapi import Form


class QuestionSchema(BaseModel):
    question: str

    @classmethod
    def as_form(
            cls,
            question: str = Form(...),
    ):
        return cls(question=question)
