from pydantic import BaseModel, field_validator, Field

from app.core.mixins import EmailMixin


class EmailSchema(EmailMixin, BaseModel):
    pass


class RegisterSchema(EmailMixin, BaseModel):
    first_name: str = Field(min_length=1, max_length=50)
    last_name: str = Field(min_length=1, max_length=50)
    password: str = Field(min_length=8, max_length=16)


class TokenSchema(BaseModel):
    token: str


class VerifySchema(EmailMixin, BaseModel):
    code: str


class LoginSchema(EmailMixin, BaseModel):
    password: str
