from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from app.core.db import get_session
from app.schemas.user_info_schema import UserInfoSchema
from app.services.user_service import UserService

router = APIRouter(prefix="/v1")


@router.get("/userinfo", response_model=UserInfoSchema)
def get_userinfo(
    user_id: str,
    session: Session = Depends(get_session),
):
    user_service = UserService(session)
    user_info = user_service.get_userinfo(user_id)
    if not user_info:
        raise HTTPException(status_code=404, detail="User not found")
    return user_info
