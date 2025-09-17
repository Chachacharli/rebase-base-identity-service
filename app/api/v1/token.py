import base64
import hashlib
from datetime import datetime, timedelta

from fastapi import APIRouter, Form, HTTPException
from jose import jwt

from app.core.config import settings
from app.core.store import validate_authorization_code

# Tiempo de vida de access_token
ACCESS_TOKEN_TTL = timedelta(minutes=30)

router = APIRouter()


@router.post("/token")
def token(
    grant_type: str = Form(...),
    code: str = Form(...),
    redirect_uri: str = Form(...),
    client_id: str = Form(...),
    code_verifier: str = Form(...),
):
    if grant_type != "authorization_code":
        raise HTTPException(status_code=400, detail="Unsupported grant_type")
    # Validar authorization code
    data = validate_authorization_code(code)
    if not data:
        raise HTTPException(status_code=400, detail="Invalid or expired code")

    # Validar redirect_uri y client_id
    if data["redirect_uri"] != redirect_uri or data["client_id"] != client_id:
        raise HTTPException(status_code=400, detail="Invalid client or redirect_uri")

    hashed = hashlib.sha256(code_verifier.encode()).digest()
    calc_challenge = base64.urlsafe_b64encode(hashed).rstrip(b"=").decode()
    if calc_challenge != data["code_challenge"]:
        raise HTTPException(status_code=400, detail="Invalid PKCE code_verifier")

    # Generar access_token / id_token
    payload = {
        "sub": "user123",
        "iss": settings.BASE_URL,
        "aud": client_id,
        "exp": datetime.utcnow() + ACCESS_TOKEN_TTL,
        "iat": datetime.utcnow(),
    }

    access_token = jwt.encode(
        payload, open(settings.PRIVATE_KEY_PATH).read(), algorithm="RS256"
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": int(ACCESS_TOKEN_TTL.total_seconds()),
        "id_token": access_token,
        "scope": data["scope"],
    }
