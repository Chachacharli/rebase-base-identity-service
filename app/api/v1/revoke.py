from fastapi import APIRouter, Form

router = APIRouter()

# Aquí deberías tener un "store" que permita invalidar tokens (lista negra o estado en BD)
revoked_tokens = set()


@router.post("/revoke")
def revoke(token: str = Form(...), token_type_hint: str = Form(None)):
    # Guardar en tu blacklist de tokens
    revoked_tokens.add(token)
    return {"revoked": True}
