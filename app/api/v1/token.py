from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, Form, HTTPException

from app.core.config import settings
from app.core.db import get_session
from app.domain.grants.grant_types import GrantType
from app.domain.tokens.authorization_code_grant_request import (
    AuthorizationCodeGrantRequest,
)
from app.models.refresh_token import RefreshToken
from app.repositories.refresh_token_repository import RefreshTokenRepository
from app.services.grants.authorization_code_grant_handler import (
    AuthorizationCodeGrantHandler,
)

router = APIRouter()


grant_handlers = {
    GrantType.AUTHORIZATION_CODE: AuthorizationCodeGrantHandler(settings),
}


@router.post("/token")
def token(
    grant_type: str = Form(...),
    code: str = Form(...),
    redirect_uri: str = Form(...),
    client_id: str = Form(None),
    code_verifier: str = Form(...),
    refresh_token: str = Form(None),
    session=Depends(get_session),
):
    request = AuthorizationCodeGrantRequest(
        grant_type=grant_type,
        code=code,
        redirect_uri=redirect_uri,
        client_id=client_id,
        code_verifier=code_verifier,
        refresh_token=refresh_token,
    )

    handler = grant_handlers.get(grant_type)

    if not handler:
        raise HTTPException(status_code=400, detail="Unsupported grant_type")

    tokens = handler.handle(request)

    # Guardamos el refresh token en la base de datos
    if tokens.refresh_token:
        refresh_token_obj = RefreshToken(
            token=tokens.refresh_token,
            user_id=tokens.user_id,
            client_id=client_id,
            scope=tokens.scope,
            expires_at=datetime.now(timezone.utc)
            + timedelta(seconds=tokens.expires_in),
            revoked=False,
        )
        repo = RefreshTokenRepository(session)
        repo.save(refresh_token_obj)

    return tokens
