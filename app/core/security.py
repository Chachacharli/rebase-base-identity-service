from cryptography.hazmat.primitives import serialization
from jose.utils import base64url_encode

from app.core.config import Settings

path = Settings().PRIVATE_KEY_PATH

# Cargar tu llave privada desde el archivo .pem
with open(str(path), "rb") as key_file:
    private_key = serialization.load_pem_private_key(
        key_file.read(),
        password=None,
    )

public_key = private_key.public_key()


def get_jwk():
    numbers = public_key.public_numbers()
    e = base64url_encode(numbers.e.to_bytes((numbers.e.bit_length() + 7) // 8, "big"))
    n = base64url_encode(numbers.n.to_bytes((numbers.n.bit_length() + 7) // 8, "big"))

    return {
        "kty": "RSA",
        "use": "sig",
        "alg": "RS256",
        "kid": "102f6d18-6089-43e7-b01e-cbb74c6bb68d",
        "n": n.decode("utf-8"),
        "e": e.decode("utf-8"),
    }
