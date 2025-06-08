from pydantic import BaseModel, EmailStr, field_validator


class EmailSchema(BaseModel):
    email: EmailStr


class RegisterSchema(EmailSchema):
    first_name: str
    last_name: str
    password: str


    @field_validator("password")
    def validate_password(cls, v):
        if len(v) < 6:
            raise ValueError("Password must be at least 6 characters")
        return v


class TokenSchema(BaseModel):
    token: str


class VerifySchema(EmailSchema):
    code: str


class LoginSchema(EmailSchema):
    password: str
