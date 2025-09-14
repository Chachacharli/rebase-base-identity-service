from jose import jwk
from jose.utils import base64url_encode

from app.core.config import settings


def load_public_key():
    with open(settings.PUBLIC_KEY_PATH, "rb") as f:
        return f.read()


def get_jwk():
    """Convierte la clave pública en formato JWK para /.well-known/jwks.json"""
    public_key = load_public_key()
    jwk_key = jwk.construct(public_key, algorithm=settings.JWT_ALG)

    return {
        "kty": jwk_key._params["kty"],
        "n": base64url_encode(jwk_key._params["n"]),
        "e": base64url_encode(jwk_key._params["e"]),
        "alg": settings.JWT_ALG,
        "use": "sig",
        "kid": "auth-service-key-1",
    }
