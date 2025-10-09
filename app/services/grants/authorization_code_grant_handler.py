import base64
import hashlib
import secrets
from datetime import datetime, timedelta

from fastapi import HTTPException
from jose import jwt

from app.core.config import Settings
from app.core.store import authorization_code_store
from app.domain.tokens.authorization_code_grant_request import (
    AuthorizationCodeGrantRequest,
)
from app.domain.tokens.id_token_payload import IDTokenPayload
from app.domain.tokens.token_response import GrantTokenResponse
from app.services.grants.token_grant_handler import TokenGrantHandler

REFRESH_TOKEN_TTL = 60 * 60 * 24 * 1
ACCESS_TOKEN_TTL = timedelta(minutes=30)


class AuthorizationCodeGrantHandler(TokenGrantHandler):
    def __init__(self, settings: Settings):
        self.settings = settings

    def handle(self, form_data: AuthorizationCodeGrantRequest) -> GrantTokenResponse:
        code = form_data.code
        redirect_uri = form_data.redirect_uri
        client_id = form_data.client_id
        code_verifier = form_data.code_verifier

        data = authorization_code_store.validate(code)
        if not data:
            raise HTTPException(status_code=400, detail="Invalid or expired code")

        if data.redirect_uri != redirect_uri or data.client_id != client_id:
            raise HTTPException(
                status_code=400, detail="Invalid client or redirect_uri"
            )

        hashed = hashlib.sha256(code_verifier.encode()).digest()
        calc_challenge = base64.urlsafe_b64encode(hashed).rstrip(b"=").decode()
        if calc_challenge != data.code_challenge:
            raise HTTPException(status_code=400, detail="Invalid PKCE code_verifier")

        access_token = secrets.token_urlsafe(32)

        id_token_payload = IDTokenPayload(
            iss=self.settings.BASE_URL,
            sub=str(data.user_id),
            aud=client_id,
            exp=datetime.utcnow() + timedelta(minutes=30),
            iat=datetime.utcnow(),
        )

        id_token = jwt.encode(
            id_token_payload.to_dict(),
            open(self.settings.PRIVATE_KEY_PATH).read(),
            algorithm="RS256",
        )

        # Generar refresh token (simple, sin JWT)
        refresh_token = secrets.token_urlsafe(32)

        response = GrantTokenResponse(
            access_token=access_token,
            user_id=data.user_id,
            client_id=client_id,
            token_type="bearer",
            expires_in=int(ACCESS_TOKEN_TTL.total_seconds()),
            id_token=id_token,
            refresh_token=refresh_token,
            scope=data.scope,
        )

        return response
