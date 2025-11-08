from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, Form, HTTPException

from app.core.config import settings
from app.core.db import Session, get_session
from app.domain.grants.grant_types import GrantType
from app.domain.tokens.authorization_code_grant_request import (
    AuthorizationCodeGrantRequest,
)
from app.models.access_token import AccessToken
from app.models.refresh_token import RefreshToken
from app.repositories.access_token_repository import AccessTokenRepository
from app.repositories.refresh_token_repository import RefreshTokenRepository
from app.services.grants.authorization_code_grant_handler import (
    AuthorizationCodeGrantHandler,
)
from app.services.grants.refresh_token_grant_handler import RefreshTokenGrantHandler
from app.services.token_service import TokenService

router = APIRouter()


grant_handlers = {
    GrantType.AUTHORIZATION_CODE: AuthorizationCodeGrantHandler,
    GrantType.REFRESH_TOKEN: RefreshTokenGrantHandler,
}


@router.post("/token")
def token(
    grant_type: str = Form(...),
    code: str = Form(None),
    redirect_uri: str = Form(None),
    client_id: str = Form(...),
    code_verifier: str = Form(None),
    refresh_token: str = Form(None),
    session: Session = Depends(get_session),
):
    # Initialize TokenService
    svc = TokenService(session)

    if grant_type == GrantType.AUTHORIZATION_CODE:
        handler = AuthorizationCodeGrantHandler(settings, session)

        request = AuthorizationCodeGrantRequest(
            grant_type=grant_type,
            code=code,
            redirect_uri=redirect_uri,
            client_id=client_id,
            code_verifier=code_verifier,
        )
        tokens = handler.handle(request)

        # Save Refresh token
        rt_repo = RefreshTokenRepository(session)
        refresh_token = RefreshToken(
            token=tokens.refresh_token,
            user_id=tokens.user_id,
            client_id=client_id,
            scope=tokens.scope,
            expires_at=datetime.now(timezone.utc)
            + timedelta(seconds=tokens.expires_in),
            revoked=False,
        )

        refresh_token = rt_repo.create(refresh_token)

        # Save Access token
        at_repo = AccessTokenRepository(session)
        access_obj = AccessToken(
            token=tokens.access_token,
            user_id=tokens.user_id,
            client_id=client_id,
            scope=tokens.scope,
            expires_at=datetime.now(timezone.utc)
            + timedelta(seconds=tokens.expires_in),
            refresh_token_id=refresh_token.id,
        )
        at_repo.create(access_obj)

        return tokens

    elif grant_type == GrantType.REFRESH_TOKEN:
        try:
            result = svc.refresh_with_rotation(refresh_token, client_id)
            session.commit()
        except ValueError:
            session.rollback()
            raise HTTPException(status_code=400, detail="invalid_grant")
        return result

    else:
        raise HTTPException(status_code=400, detail="unsupported_grant_type")
