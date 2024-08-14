from typing import List
from pydantic import EmailStr
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from schemas.users import UserSchemaOut, UserSchemaIn
from models.users import UserModel
from config.database import get_db_session

router = APIRouter()


@router.get("", response_model=List[UserSchemaOut])
async def get_all_users(db: Session = Depends(get_db_session)):
    return UserModel.get_all_users(db)


@router.get("/email", response_model=UserSchemaOut)
async def get_user_by_email(email: EmailStr, db: Session = Depends(get_db_session)):
    return UserModel.get_user_by_email(email, db)


@router.post("", response_model=UserSchemaOut)
async def create_user(user: UserSchemaIn, db: Session = Depends(get_db_session)):
    if UserModel.check_user_by_email(user.email, db):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Email {user.email} already registered')
    return UserModel.create_user(user, db)
