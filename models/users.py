from typing import List

from pydantic import EmailStr
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Session

from config.database import Base
from schemas.users import UserSchemaIn


class UserModel(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, unique=True, nullable=False)

    @classmethod
    def create(cls, user: UserSchemaIn, db: Session) -> "UserModel":
        user = cls(**user.model_dump())
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    @classmethod
    def get_all(cls, db: Session) -> List["UserModel"]:
        return db.query(cls).order_by(cls.id).all()

    @classmethod
    def get_by_email(cls, email: EmailStr, db: Session) -> "UserModel":
        return db.query(cls).filter_by(email=email).first()

    @classmethod
    def validate_by_email(cls, email: str, db: Session) -> bool:
        user = cls.get_by_email(email, db)
        return True if user else False
