from pydantic import BaseModel, EmailStr, Field, ConfigDict


class CreateUserSchema(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    password: str = Field(min_length=8, max_length=16)


class ListUsersSchema(BaseModel):
    id: int
    email: EmailStr
    first_name: str
    last_name: str
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


class StudentSchema(BaseModel):
    id: int
    email: EmailStr
    first_name: str
    last_name: str
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


class GetUsersSchema(BaseModel):
    total: int
    pages: int
    limit: int
    users: list[ListUsersSchema]


class MeSchema(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str

    model_config = ConfigDict(from_attributes=True)


class CreateStudentSchema(CreateUserSchema):
    pass



