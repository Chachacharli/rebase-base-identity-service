import base64
import hashlib
from datetime import datetime, timedelta
from typing import Any, Dict

from fastapi import HTTPException
from jose import jwt

from app.core.config import Settings
from app.core.store import validate_authorization_code

REFRESH_TOKEN_TTL = 60 * 60 * 24 * 1
ACCESS_TOKEN_TTL = timedelta(minutes=30)


class AuthorizationCodeGrantHandler:
    def __init__(self, settings: Settings):
        self.settings = settings

    def handle(self, form_data: Dict[str, Any]) -> Dict[str, Any]:
        code = form_data["code"]
        redirect_uri = form_data["redirect_uri"]
        client_id = form_data["client_id"]
        code_verifier = form_data["code_verifier"]

        data = validate_authorization_code(code)
        if not data:
            raise HTTPException(status_code=400, detail="Invalid or expired code")

        if data["redirect_uri"] != redirect_uri or data["client_id"] != client_id:
            raise HTTPException(
                status_code=400, detail="Invalid client or redirect_uri"
            )

        hashed = hashlib.sha256(code_verifier.encode()).digest()
        calc_challenge = base64.urlsafe_b64encode(hashed).rstrip(b"=").decode()
        if calc_challenge != data["code_challenge"]:
            raise HTTPException(status_code=400, detail="Invalid PKCE code_verifier")

        access_payload = {
            "sub": data["user_id"],
            "iss": self.settings.BASE_URL,
            "aud": client_id,
            "exp": datetime.utcnow() + timedelta(seconds=30),
            "iat": datetime.utcnow(),
        }
        access_token = jwt.encode(
            access_payload,
            open(self.settings.PRIVATE_KEY_PATH).read(),
            algorithm="RS256",
        )

        refresh_payload = {
            "sub": data["user_id"],
            "iss": self.settings.BASE_URL,
            "aud": client_id,
            "exp": datetime.utcnow() + timedelta(seconds=REFRESH_TOKEN_TTL),
            "iat": datetime.utcnow(),
            "typ": "refresh",
        }
        refresh_token_jwt = jwt.encode(
            refresh_payload,
            open(self.settings.PRIVATE_KEY_PATH).read(),
            algorithm="RS256",
        )

        return {
            "access_token": access_token,
            "token_type": "bearer",
            "expires_in": int(ACCESS_TOKEN_TTL.total_seconds()),
            "id_token": access_token,
            "refresh_token": refresh_token_jwt,
            "scope": data["scope"],
        }
