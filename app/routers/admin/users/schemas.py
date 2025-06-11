from pydantic import BaseModel, EmailStr, Field, ConfigDict


class CreateUserSchema(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    password: str = Field(min_length=8, max_length=16)


class UserSchema(BaseModel):
    id: int
    email: EmailStr
    first_name: str
    last_name: str

    model_config = ConfigDict(from_attributes=True)


class GetUsersSchema(BaseModel):
    total: int
    pages: int
    limit: int
    results: list[UserSchema]
