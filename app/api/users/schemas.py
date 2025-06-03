from pydantic import BaseModel, ConfigDict, EmailStr


class NameSchema(BaseModel):
    first_name: str
    last_name: str


class MeSchema(NameSchema):
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)
