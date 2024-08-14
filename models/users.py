from sqlalchemy import Column, Integer, String
from schemas.users import UserSchemaIn
from sqlalchemy.orm import Session
from pydantic import EmailStr
from config.database import Base


class UserModel(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, unique=True, nullable=False)

    @classmethod
    def create_user(cls, user: UserSchemaIn, db: Session):
        user = cls(**user.dict())
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    @classmethod
    def get_all_users(cls, db: Session):
        return db.query(cls).order_by(cls.id.desc()).all()

    @classmethod
    def get_user_by_email(cls, email: EmailStr, db: Session):
        return db.query(cls).filter_by(email=email).first()

    @classmethod
    def check_user_by_email(cls, email: str, db: Session):
        user = cls.get_user_by_email(email, db)
        return True if user else False
