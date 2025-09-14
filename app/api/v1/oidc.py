from fastapi import APIRouter

from app.core.config import settings
from app.core.security import get_jwk

router = APIRouter()


@router.get("/.well-known/openid-configuration")
def openid_configuration():
    return {
        "issuer": settings.BASE_URL,
        "authorization_endpoint": f"{settings.BASE_URL}/authorize",
        "token_endpoint": f"{settings.BASE_URL}/token",
        "userinfo_endpoint": f"{settings.BASE_URL}/userinfo",
        "jwks_uri": f"{settings.BASE_URL}/jwks.json",
        "revocation_endpoint": f"{settings.BASE_URL}/revocation",
        "response_types_supported": ["code", "id_token", "token id_token"],
        "subject_types_supported": ["public"],
        "id_token_signing_alg_values_supported": [settings.JWT_ALG],
        "scopes_supported": ["openid", "profile", "email"],
        "token_endpoint_auth_methods_supported": ["client_secret_basic", "none"],
    }


@router.get("/jwks.json")
def jwks():
    return {"keys": [get_jwk()]}
