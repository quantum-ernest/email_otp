from pydantic import BaseModel
from pydantic import EmailStr


class UserSchemaIn(BaseModel):
    email: EmailStr


class UserSchemaOut(UserSchemaIn):
    id: int


