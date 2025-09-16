from uuid import uuid4

from fastapi import APIRouter, HTTPException
from fastapi.responses import RedirectResponse

from app.core.store import save_authorization_code

router = APIRouter()

# Simulación de clientes registrados
CLIENTS = {
    "my-spa-client": {
        "redirect_uris": [
            "http://localhost:3000/callback",
            "https://oauth.pstmn.io/v1/callback",
        ]
    }
}


@router.get("/authorize")
def authorize(
    response_type: str,
    client_id: str,
    redirect_uri: str,
    scope: str,
    state: str,
    code_challenge: str,
    code_challenge_method: str = "S256",
):
    # Validar client_id
    client = CLIENTS.get(client_id)
    if not client:
        raise HTTPException(status_code=400, detail="Invalid client_id")

    # Validar redirect_uri
    if redirect_uri not in client["redirect_uris"]:
        raise HTTPException(status_code=400, detail="Invalid redirect_uri")

    # Generar authorization code
    auth_code = str(uuid4())
    save_authorization_code(auth_code, client_id, redirect_uri, code_challenge)

    # Redirigir al cliente con code + state
    redirect_url = f"{redirect_uri}?code={auth_code}&state={state}"
    return RedirectResponse(redirect_url)
