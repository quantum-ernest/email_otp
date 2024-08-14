from fastapi import APIRouter, Depends, HTTPException, status
from schemas.auth import OtpGenerateSchemaIn, OtpGenerateSchemaOut, OtpLoginSchemaIn, OtpLoginSchemaOut
from sqlalchemy.orm import Session
from config.database import get_db_session
from models.users import UserModel
from services.auth import AuthService

router = APIRouter()


@router.post("/generates", response_model=OtpGenerateSchemaOut)
async def generate_otp(credentials: OtpGenerateSchemaIn, db: Session = Depends(get_db_session)):
    if not (UserModel.check_user_by_email(credentials.email, db)):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'User with Email {credentials.email} not found')
    return await AuthService.generate_otp_via_email(credentials.email)


@router.post("/login", response_model=OtpLoginSchemaOut)
async def login(credential: OtpLoginSchemaIn, db: Session = Depends(get_db_session)):
    user = UserModel.get_user_by_email(credential.email, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with email {credential.email} not found",
        )
    return AuthService.otp_login_via_email(credential, user)
