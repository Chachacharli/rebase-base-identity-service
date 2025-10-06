from datetime import datetime, timezone

from fastapi import APIRouter, Depends, Form
from jose import JWTError, jwt
from sqlmodel import Session

from app.core.config import settings
from app.core.db import get_session
from app.repositories.refresh_token_repository import RefreshTokenRepository

router = APIRouter()


@router.post("/introspect")
def introspect(token: str = Form(...), session: Session = Depends(get_session)):
    try:
        payload = jwt.decode(
            token,
            open(settings.PUBLIC_KEY_PATH).read(),
            algorithms=["RS256"],
            options={"verify_aud": False},
        )
        return {"active": True, **payload}
    except JWTError:
        # Revisar si es refresh token en DB
        repo = RefreshTokenRepository(session)
        db_token = repo.get(token)

        if (
            db_token
            and not db_token.revoked
            and db_token.expires_at > datetime.now(timezone.utc)
        ):
            return {"active": True, "sub": db_token.user_id, "typ": "refresh"}
        return {"active": False}
