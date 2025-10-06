from fastapi import APIRouter

from app.api.v1.auth import router as auth_router
from app.api.v1.client_application import router as client_application_router
from app.api.v1.introspect import router as introspect_router
from app.api.v1.oidc import router as oidc_router
from app.api.v1.revoke import router as revoke_router
from app.api.v1.token import router as token_router
from app.api.v1.user import router as user_router

api_router = APIRouter()

api_router.include_router(oidc_router, prefix="/oidc", tags=["oidc"])
api_router.include_router(auth_router, tags=["auth"])
api_router.include_router(token_router, tags=["token"])
api_router.include_router(client_application_router, tags=["Client Applications"])
api_router.include_router(introspect_router, tags=["introspect"])
api_router.include_router(revoke_router, tags=["revoke"])
api_router.include_router(user_router, tags=["user"])
