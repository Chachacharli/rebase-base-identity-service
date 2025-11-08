import base64
import hashlib
from datetime import datetime, timedelta

from fastapi import HTTPException
from jose import jwt

from app.core.store import authorization_code_store
from app.domain.tokens.authorization_code_grant_request import (
    AuthorizationCodeGrantRequest,
)
from app.domain.tokens.id_token_payload import IDTokenPayload
from app.domain.tokens.token_response import GrantTokenResponse
from app.repositories.app_settings_repository import AppSettingRepository
from app.services.grants.token_grant_handler import TokenGrantHandler
from app.services.token_service import TokenService


class AuthorizationCodeGrantHandler(TokenGrantHandler):
    def handle(self, form_data: AuthorizationCodeGrantRequest) -> GrantTokenResponse:
        data = authorization_code_store.validate(form_data.code)
        if not data:
            raise HTTPException(status_code=400, detail="Invalid or expired code")

        if (
            data.redirect_uri != form_data.redirect_uri
            or data.client_id != form_data.client_id
        ):
            raise HTTPException(
                status_code=400, detail="Invalid client or redirect_uri"
            )

        hashed = hashlib.sha256(form_data.code_verifier.encode()).digest()
        calc_challenge = base64.urlsafe_b64encode(hashed).rstrip(b"=").decode()
        if calc_challenge != data.code_challenge:
            raise HTTPException(status_code=400, detail="Invalid PKCE code_verifier")

        # Create tokens from TokenService
        token_service = TokenService(self.session)
        token_pair = token_service.issue_tokens(
            user_id=data.user_id, client_id=form_data.client_id, scope=data.scope
        )

        # Create ID Token
        app_settings = AppSettingRepository(self.session)
        ttl_access_token = int(app_settings.get("ttl_access_token", 1800))
        id_token_payload = IDTokenPayload(
            iss=self.settings.BASE_URL,
            sub=str(data.user_id),
            aud=form_data.client_id,
            exp=datetime.utcnow() + timedelta(seconds=ttl_access_token),
            iat=datetime.utcnow(),
        )

        id_token = jwt.encode(
            id_token_payload.to_dict(),
            open(self.settings.PRIVATE_KEY_PATH).read(),
            algorithm="RS256",
        )

        # Create uniform response
        return GrantTokenResponse(
            access_token=token_pair.access_token,
            token_type="bearer",
            expires_in=token_pair.expires_in,
            id_token=id_token,
            refresh_token=token_pair.refresh_token,
            scope=data.scope,
            user_id=data.user_id,
            client_id=form_data.client_id,
        )
