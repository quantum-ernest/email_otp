"""
User API Endpoints

This module defines the API endpoints for managing user resources, including
retrieving all users, fetching a user by email, and creating a new user.

Endpoints:
    - GET /: Retrieve all users.
    - GET /email: Retrieve a user by their email.
    - POST /: Create a new user.

Dependencies:
    - FastAPI: Web framework for building APIs.
    - SQLAlchemy ORM: Used for database operations.
    - Pydantic: Data validation and settings management using Python type annotations.

Schemas:
    - UserSchemaOut: Output schema for user data.
    - UserSchemaIn: Input schema for user creation.

Models:
    - UserModel: SQLAlchemy model representing a user.

Exceptions:
    - HTTPException: Raised when attempting to create a user with an already registered email.
"""

from typing import List
from pydantic import EmailStr
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from schemas.users import UserSchemaOut, UserSchemaIn
from models.users import UserModel
from config.database import get_db_session

router = APIRouter()


@router.get("", response_model=List[UserSchemaOut])
async def get_all(db: Session = Depends(get_db_session)):
    """
    Retrieve all users from the database.

    Args:
        db (Session): SQLAlchemy session dependency.

    Returns:
        List[UserSchemaOut]: A list of all users.
    """
    return UserModel.get_all(db)


@router.get("/email", response_model=UserSchemaOut)
async def get_by_email(email: EmailStr, db: Session = Depends(get_db_session)):
    """
    Retrieve a user by their email address.

    Args:
        email (EmailStr): The email of the user to retrieve.
        db (Session): SQLAlchemy session dependency.

    Returns:
        UserSchemaOut: The user data associated with the given email.
    """
    return UserModel.get_by_email(email, db)


@router.post("", response_model=UserSchemaOut)
async def create_user(user: UserSchemaIn, db: Session = Depends(get_db_session)):
    """
    Create a new user in the database.

    Args:
        user (UserSchemaIn): Input schema for creating a new user.
        db (Session): SQLAlchemy session dependency.

    Returns:
        UserSchemaOut: The newly created user's data.

    Raises:
        HTTPException: If the email is already registered.
    """
    if UserModel.validate_by_email(user.email, db):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Email {user.email} already registered",
        )
    return UserModel.create(user, db)
