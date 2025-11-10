from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlmodel import Session

from app.core.db import get_session
from app.exceptions.bussiness_exceptions import (
    RequiredPermissionException,
    RequiredRoleException,
)
from app.exceptions.http_exceptions import UnauthorizedException
from app.models.user import User
from app.repositories.access_token_repository import AccessTokenRepository
from app.services.user_service import UserService

oauth2_scheme = HTTPBearer()


def get_current_user(
    token: HTTPAuthorizationCredentials = Depends(oauth2_scheme),
    session: Session = Depends(get_session),
) -> User:
    """Retrieve the current authenticated user based on the provided token."""
    access_token_repo = AccessTokenRepository(session)
    user_service = UserService(session)
    access_token = access_token_repo.get(token.credentials)
    if not access_token or access_token.revoked:
        raise UnauthorizedException("Invalid authentication credentials")
    user = user_service.get_user_by_id(access_token.user_id)
    if not user:
        raise UnauthorizedException("Invalid user")
    return user


def require_role(required_role: str) -> User:
    """Required specific role."""

    def wrapper(user: User = Depends(get_current_user)):
        roles = [role.name for role in user.roles]
        if required_role not in roles:
            raise RequiredRoleException(required_role)
        return user

    return wrapper


def require_roles(required_roles: list[str]) -> User:
    """Required any of the roles in the list."""

    def wrapper(user: User = Depends(get_current_user)):
        roles = [role.name for role in user.roles]
        if not any(role in roles for role in required_roles):
            raise RequiredRoleException(required_roles)
        return user

    return wrapper


def require_permission(required_permission: str) -> User:
    """Required specific permission."""

    def wrapper(user: User = Depends(get_current_user)):
        permissions = [perm.name for role in user.roles for perm in role.permissions]
        if required_permission not in permissions:
            raise RequiredPermissionException(required_permission)
        return user

    return wrapper
