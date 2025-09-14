from fastapi import APIRouter

from app.api.v1.auth import router as auth_router
from app.api.v1.oidc import router as oidc_router
from app.api.v1.token import router as token_router

api_router = APIRouter()

api_router.include_router(oidc_router, prefix="/oidc", tags=["oidc"])
api_router.include_router(auth_router, prefix="/auth", tags=["auth"])
api_router.include_router(token_router, prefix="/token", tags=["token"])
