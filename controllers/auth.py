from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from config.database import get_db_session
from models.users import UserModel
from schemas.auth import (
    OtpGenerateSchemaIn,
    OtpGenerateSchemaOut,
    OtpLoginSchemaIn,
    OtpLoginSchemaOut,
)
from schemas.users import UserSchemaIn
from services.auth import AuthService

router = APIRouter()


@router.post("/generates", response_model=OtpGenerateSchemaOut)
async def generate_otp(
    credentials: OtpGenerateSchemaIn, db: Session = Depends(get_db_session)
):
    """
    Generate a One-Time Password (OTP) for user authentication via email.

    Args:
        credentials (OtpGenerateSchemaIn): Input schema for OTP generation request.
        db (Session): SQLAlchemy session dependency.

    Returns:
        OtpGenerateSchemaOut: Output schema for OTP generation response.
    """
    val_user = UserModel.validate_by_email(credentials.email, db)
    if val_user is False:
        user_object = UserSchemaIn(email=credentials.email)
        user = UserModel.create(user_object, db)
        return await AuthService.generate_otp_via_email(user.email)
    return await AuthService.generate_otp_via_email(credentials.email)


@router.post("/login", response_model=OtpLoginSchemaOut)
async def login(credential: OtpLoginSchemaIn, db: Session = Depends(get_db_session)):
    """
    Authenticate a user using the generated OTP.

    Args:
        credential (OtpLoginSchemaIn): Input schema for OTP login request.
        db (Session): SQLAlchemy session dependency.

    Returns:
        OtpLoginSchemaOut: Output schema for OTP login response.

    Raises:
        HTTPException: If the user with the given email is not found.
    """
    user = UserModel.get_by_email(credential.email, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with email {credential.email} not found",
        )
    return AuthService.otp_login_via_email(credential, user)
