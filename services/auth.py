import redis
from fastapi import HTTPException, status
from fastapi_mail import MessageSchema
from jose import JWTError, jwt
from pydantic import EmailStr

from config.env import envConfig
from schemas.auth import OtpLoginSchemaIn
from services.mail import MailService
from utils.mail_templates import login_otp_template
from utils.random_otp import generate_otp

_redis = redis.Redis(
    host=envConfig.REDIS_HOST, port=envConfig.REDIS_PORT, decode_responses=True
)
mail_service = MailService()


class AuthService:
    """Service class handling authentication-related operations."""

    @classmethod
    def create_access_token(cls, data: dict) -> str:
        """
        Creates a JWT access token.

        Args:
            data (dict): The data to encode in the JWT.

        Returns:
            str: The encoded JWT.
        """
        encoded_jwt = jwt.encode(
            data.copy(), envConfig.AUTH_SECRETE_KEY, algorithm=envConfig.AUTH_ALGORITHM
        )
        return encoded_jwt

    @classmethod
    def get_access_token(cls, user) -> dict:
        """
        Generates an access token for a user.

        Args:
            user: The user object.

        Returns:
            dict: A dictionary containing the access token.
        """
        token = cls.create_access_token(
            data={
                "id": user.id,
                "email": user.email,
            }
        )
        return {"token": token}

    @classmethod
    def decode_token(cls, token: str) -> dict:
        """
        Decodes a JWT token.

        Args:
            token (str): The JWT token to decode.

        Returns:
            dict: The decoded token data.

        Raises:
            JWTError: If the token is invalid or cannot be decoded.
        """
        try:
            return jwt.decode(
                token, envConfig.AUTH_SECRETE_KEY, algorithms=[envConfig.AUTH_ALGORITHM]
            )
        except JWTError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid Token: {e}"
            )

    @classmethod
    def otp_login_via_email(cls, credential: OtpLoginSchemaIn, user) -> dict:
        """
        Handles OTP login via email.

        Args:
            credential (OtpLoginSchemaIn): The OTP login credentials.
            user: The user object.

        Returns:
            dict: A dictionary containing the access token.

        Raises:
            HTTPException: If the OTP is incorrect.
        """
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
        """
        Verifies the OTP for a given email.

        Args:
            credential (OtpLoginSchemaIn): The OTP login credentials.

        Returns:
            bool: True if the OTP is correct, False otherwise.
        """
        return True if (_redis.get(name=credential.email) == credential.otp) else False

    @classmethod
    async def generate_otp_via_email(cls, email: EmailStr) -> dict:
        """
        Generates and sends an OTP via email.

        Args:
            email (EmailStr): The email address to send the OTP to.

        Returns:
            dict: A success message indicating that the OTP was sent.
        """
        await cls.send_otp_via_email(email)
        return {"message": "OTP sent successfully"}

    @classmethod
    async def send_otp_via_email(cls, email: EmailStr) -> bool:
        """
        Sends an OTP via email.

        Args:
            email (EmailStr): The email address to send the OTP to.

        Returns:
            bool: True if the OTP was sent successfully.

        Raises:
            HTTPException: If there is an error sending the email.
        """
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
