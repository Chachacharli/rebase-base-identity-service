from fastapi import APIRouter

from app.api.v1.oidc import router as oidc_router

api_router = APIRouter()

api_router.include_router(oidc_router, prefix="/oidc", tags=["oidc"])
