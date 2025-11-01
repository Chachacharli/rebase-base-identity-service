from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from app.core.db import get_session
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


@router.get("/user/{user_id}", response_model=UserRead)
def get_user(user_id: UUID, db: Session = Depends(get_session)):
    user_service = UserService(db)
    user = user_service.get_user_by_id(user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return UserRead.from_orm(user)


@router.get("/user", response_model=list[UserRead])
def list_users(db: Session = Depends(get_session)):
    user_service = UserService(db)
    users = user_service.get_all_users()
    return [UserRead.model_validate(user) for user in users]


@router.put("/user/{user_id}", response_model=UserRead)
def update_user(
    user_id: UUID, user_update: UserUpdate, db: Session = Depends(get_session)
):
    # TODO: implement update logic
    pass


@router.delete("/user/{user_id}")
def delete_user(user_id: UUID, db: Session = Depends(get_session)):
    # TODO: implemente soft delete logic
    pass


@router.post("/user/{user_id}/set_role")
def set_user_role(user_id: UUID, role_id: UUID, db: Session = Depends(get_session)):
    # TODO: Implement set role logic
    pass
