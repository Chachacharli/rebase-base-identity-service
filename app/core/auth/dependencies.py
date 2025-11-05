from fastapi import Depends, HTTPException, status
from sqlmodel import Session

from app.core.db import get_session
from app.models.user import User
from app.services.user_service import UserService


def get_current_user(
    token: str = Depends(...), db: Session = Depends(get_session)
) -> User:
    """Retrieve the current authenticated user based on the provided token."""
    # Implementation to retrieve user from token goes here
    ...


def require_role(required_role: str):
    """Required specific role."""

    def wrapper(user: User = Depends(...)):
        roles = [role.name for role in user.roles]
        if required_role not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Role '{required_role}' required",
            )
        return user

    return wrapper


def require_roles(required_roles: list[str]):
    """Required any of the roles in the list."""

    def wrapper(user: User = Depends(...)):
        roles = [role.name for role in user.roles]
        if not any(role in roles for role in required_roles):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"One of the roles '{', '.join(required_roles)}' required",
            )
        return user

    return wrapper


def require_permission(required_permission: str):
    """Required specific permission."""

    def wrapper(user: User = Depends(...)):
        permissions = [perm.name for role in user.roles for perm in role.permissions]
        if required_permission not in permissions:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Permission '{required_permission}' required",
            )
        return user

    return wrapper
