from fastapi import APIRouter, Form
from jose import JWTError, jwt

from app.core.config import settings

router = APIRouter()


@router.post("/introspect")
def introspect(token: str = Form(...)):
    try:
        payload = jwt.decode(
            token,
            open(settings.PUBLIC_KEY_PATH).read(),
            algorithms=["RS256"],
            audience=None,
            options={"verify_aud": False},
        )
        return {
            "active": True,
            "sub": payload.get("sub"),
            "exp": payload.get("exp"),
            "iss": payload.get("iss"),
            "aud": payload.get("aud"),
            "scope": payload.get("scope"),
            "typ": payload.get("typ", "access"),
        }
    except JWTError:
        return {"active": False}
