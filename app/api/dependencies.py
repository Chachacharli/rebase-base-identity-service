from typing import Optional

from fastapi import Header, HTTPException, status


def decode_token(token: str) -> dict:
    # ...implementa la lógica para decodificar el token y extraer claims...
    # Por ejemplo, usando PyJWT:
    # import jwt
    # return jwt.decode(token, "your-secret", algorithms=["HS256"])
    # Aquí solo es un ejemplo:
    return {"sub": "user_id_example"}


def get_current_user_id(authorization: Optional[str] = Header(None)) -> str:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing Authorization header",
        )
    token = authorization.split(" ", 1)[1]
    payload = decode_token(token)
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token: missing user id",
        )
    return user_id
