from fastapi import APIRouter, Depends, Form, HTTPException

from app.core.config import settings
from app.core.db import Session, get_session
from app.domain.grants.grant_types import GrantType
from app.domain.tokens.authorization_code_grant_request import (
    AuthorizationCodeGrantRequest,
)
from app.domain.tokens.token_response import FormTokenRequest
from app.services.grants.authorization_code_grant_handler import (
    AuthorizationCodeGrantHandler,
)
from app.services.grants.refresh_token_grant_handler import RefreshTokenGrantHandler
from app.services.grants.token_grant_handler import TokenGrantHandler

router = APIRouter()


grant_handlers = {
    GrantType.AUTHORIZATION_CODE: AuthorizationCodeGrantHandler,
    GrantType.REFRESH_TOKEN: RefreshTokenGrantHandler,
}


@router.post("/token")
def token(
    grant_type: str = Form(...),
    code: str = Form(None),
    redirect_uri: str = Form(None),
    client_id: str = Form(...),
    code_verifier: str = Form(None),
    refresh_token: str = Form(None),
    session: Session = Depends(get_session),
):
    handler_cls = grant_handlers.get(grant_type)
    if not handler_cls:
        raise HTTPException(status_code=400, detail="unsupported_grant_type")

    handler: TokenGrantHandler = handler_cls(settings, session)

    form_data = FormTokenRequest(
        grant_type=grant_type,
        code=code,
        redirect_uri=redirect_uri,
        client_id=client_id,
        code_verifier=code_verifier,
        refresh_token=refresh_token,
    )

    response = handler.handle(AuthorizationCodeGrantRequest(**form_data.to_dict()))
    session.commit()
    return response.to_dict()
