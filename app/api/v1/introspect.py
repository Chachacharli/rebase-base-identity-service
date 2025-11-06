from fastapi import APIRouter, Depends, Form
from sqlmodel import Session

# from app.core.config import settings
from app.core.db import get_session
from app.domain.tokens.token_response import InstrospectResponse
from app.repositories.access_token_repository import AccessTokenRepository

# from app.repositories.refresh_token_repository import RefreshTokenRepository

router = APIRouter(prefix="/v1/introspect")


@router.post("/")
def introspect(
    token: str, session: Session = Depends(get_session)
) -> InstrospectResponse:
    """Introspect access token validity"""
    at_repo = AccessTokenRepository(session)
    introspect_response = at_repo.introspect(token)
    return introspect_response
