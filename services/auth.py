import redis
from config.env import envConfig
from fastapi import HTTPException, status
from fastapi_mail import MessageSchema
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import EmailStr
from services.mail import MailService
from schemas.auth import OtpLoginSchemaIn
from utils.mail_templates import login_otp_template
from utils.random_otp import generate_otp

_redis = redis.Redis(host=envConfig.REDIS_HOST, port=envConfig.REDIS_PORT, decode_responses=True)
mail_service = MailService()


class AuthService:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    @classmethod
    def hash_password(cls, password: str) -> str:
        return cls.pwd_context.hash(password)

    @classmethod
    def verify_password(cls, plain_password: str, hashed_password: str) -> bool:
        return cls.pwd_context.verify(plain_password, hashed_password)

    @classmethod
    def create_access_token(cls, data: dict) -> str:
        encoded_jwt = jwt.encode(
            data.copy(), envConfig.AUTH_SECRETE_KEY, algorithm=envConfig.AUTH_ALGORITHM
        )
        return encoded_jwt

    @classmethod
    def get_access_token(cls, user) -> dict:
        token = cls.create_access_token(
            data={
                "id": user.id,
                "email": user.email,
            }
        )
        return {"token": token}

    @classmethod
    def decode_token(cls, token: str) -> dict:
        try:
            return jwt.decode(
                token, envConfig.AUTH_SECRETE_KEY, algorithms=[envConfig.AUTH_ALGORITHM]
            )
        except JWTError as e:
            raise JWTError(e)

    @classmethod
    def otp_login_via_email(cls, credential: OtpLoginSchemaIn, user) -> dict:
        verified_otp = cls.verity_email_otp(credential)
        if verified_otp:
            return cls.get_access_token(user)
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect Verification Code",
            )

    @classmethod
    def verity_email_otp(cls, credential: OtpLoginSchemaIn) -> bool:
        return True if (_redis.get(name=credential.email) == credential.otp) else False

    @classmethod
    async def generate_otp_via_email(cls, email: EmailStr) -> dict:
        await cls.send_otp_via_email(email)
        return {"message": "OTP sent successfully"}

    @classmethod
    async def send_otp_via_email(cls, email: EmailStr) -> bool:
        otp = generate_otp()
        _redis.setex(name=email, value=otp, time=300)
        mail_massage = MessageSchema(
            recipients=[email],
            subject="Login Verification Code",
            body=login_otp_template.replace("{{otp}}", otp),
            subtype="html",
        )
        await mail_service.send_mail(mail_massage)
        return True
