from enum import Enum

from fastapi import APIRouter, Form, HTTPException

from app.core.config import settings
from app.services.grants.AuthorizationCodeGrantHandler import (
    AuthorizationCodeGrantHandler,
)

router = APIRouter()


class GrantType(str, Enum):
    authorization_code = "authorization_code"
    refresh_token = "refresh_token"


grant_handlers = {
    GrantType.authorization_code: AuthorizationCodeGrantHandler(settings),
}


@router.post("/token")
def token(
    grant_type: str = Form(...),
    code: str = Form(...),
    redirect_uri: str = Form(...),
    client_id: str = Form(...),
    code_verifier: str = Form(...),
):
    form_data = {
        "grant_type": grant_type,
        "code": code,
        "redirect_uri": redirect_uri,
        "client_id": client_id,
        "code_verifier": code_verifier,
    }

    handler = grant_handlers.get(grant_type)
    if not handler:
        raise HTTPException(status_code=400, detail="Unsupported grant_type")

    return handler.handle(form_data)
