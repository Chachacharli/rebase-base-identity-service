from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from app.core.db import get_session
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserRead, UserUpdate
from app.services.user_service import UserService

router = APIRouter()


@router.post("/user", response_model=UserRead)
def create_user(user: UserCreate, db: Session = Depends(get_session)):
    user_service = UserService(db)
    created_user = user_service.create_user(
        email=user.email, password=user.password, username=user.username
    )

    new_user = UserRead(
        email=created_user.email, id=created_user.id, username=created_user.username
    )

    return new_user
