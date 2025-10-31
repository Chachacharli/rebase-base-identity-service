from fastapi import APIRouter

from app.api.v1.app_settings import router as app_settings_router
from app.api.v1.auth import router as auth_router
from app.api.v1.client_application import router as client_application_router
from app.api.v1.health import router as health_router
from app.api.v1.introspect import router as introspect_router
from app.api.v1.oidc import router as oidc_router
from app.api.v1.permission import router as permission_router
from app.api.v1.revoke import router as revoke_router
from app.api.v1.role import router as role_router
from app.api.v1.token import router as token_router
from app.api.v1.user import router as user_router

api_router = APIRouter()

api_router.include_router(oidc_router, prefix="/oidc", tags=["OIDC"])
api_router.include_router(auth_router, tags=["Auth"])
api_router.include_router(token_router, tags=["Token"])
api_router.include_router(client_application_router, tags=["Client Applications"])
api_router.include_router(introspect_router, tags=["Introspect"])
api_router.include_router(revoke_router, tags=["Revoke"])
api_router.include_router(user_router, tags=["User"])
api_router.include_router(app_settings_router, tags=["App Settings"])
api_router.include_router(health_router, tags=["Health"])
api_router.include_router(permission_router, tags=["Permissions"])
api_router.include_router(role_router, tags=["Roles"])
