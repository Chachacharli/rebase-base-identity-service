from fastapi import APIRouter, Depends, Form
from sqlmodel import Session

from app.core.db import get_session
from app.services.token_service import TokenService

router = APIRouter(prefix="/v1/revoke")

# Aquí deberías tener un "store" que permita invalidar tokens (lista negra o estado en BD)
revoked_tokens = set()


@router.post("/")
def revoke(
    token: str = Form(...),
    token_type_hint: str = Form(None),
    session: Session = Depends(get_session),
):
    service = TokenService(session)
    service.revoke_token(token)
    return {"revoked": True}
