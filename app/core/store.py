from datetime import datetime, timedelta
from typing import Dict

# Almacena: code -> {client_id, redirect_uri, code_challenge, expires_at}
authorization_codes: Dict[str, dict] = {}

# Duración del código (10 minutos)
CODE_TTL = timedelta(minutes=10)


def save_authorization_code(
    code: str, client_id: str, redirect_uri: str, code_challenge: str, scope=["openid"]
):
    authorization_codes[code] = {
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "code_challenge": code_challenge,
        "expires_at": datetime.utcnow() + CODE_TTL,
        "scope": scope,
    }


def validate_authorization_code(code: str):
    data = authorization_codes.get(code)
    if not data:
        return None
    if data["expires_at"] < datetime.utcnow():
        del authorization_codes[code]
        return None
    # Una vez usado, borramos el código
    del authorization_codes[code]
    return data
