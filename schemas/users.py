from pydantic import BaseModel, EmailStr


class UserSchemaIn(BaseModel):
    email: EmailStr


class UserSchemaOut(UserSchemaIn):
    id: int
