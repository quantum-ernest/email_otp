from pydantic import BaseModel, EmailStr


class OTPSchemaIn(BaseModel):
    email: EmailStr


class OtpLoginSchemaIn(BaseModel):
    email: EmailStr
    otp: str


class OtpLoginSchemaOut(BaseModel):
    token: str


class OtpGenerateSchemaIn(BaseModel):
    email: EmailStr


class OtpGenerateSchemaOut(BaseModel):
    message: str
