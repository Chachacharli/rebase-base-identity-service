from uuid import UUID

from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.core.db import get_session
from app.repositories.permission_repository import PermissionRepository
from app.schemas.permission import PermissionCreate, PermissionRead, PermissionUpdate
from app.services.permission_service import PermissionService

router = APIRouter(prefix="/v1/permissions")


@router.get("/")
def list_permissions(session: Session = Depends(get_session)):
    permission_service = PermissionService(PermissionRepository(session))
    permissions = permission_service.get_permissions()
    return permissions


@router.post("/")
def create_permission(
    permission: PermissionCreate, session: Session = Depends(get_session)
):
    permission_service = PermissionService(PermissionRepository(session))
    db_permission = permission_service.create_permission(permission)
    return PermissionRead.model_validate(db_permission)


@router.get("/{permission_id}")
def get_permission(permission_id: UUID, session: Session = Depends(get_session)):
    permission_service = PermissionService(PermissionRepository(session))
    db_permission = permission_service.get_permission(permission_id)
    return PermissionRead.model_validate(db_permission)


@router.put("/{permission_id}")
def update_permission(
    permission_id: UUID,
    permission: PermissionUpdate,
    session: Session = Depends(get_session),
):
    permission_service = PermissionService(PermissionRepository(session))
    db_permission = permission_service.update_permission(permission_id, permission)
    return PermissionRead.model_validate(db_permission)


@router.delete("/{permission_id}")
def delete_permission(permission_id: UUID):
    # soft delete
    return {"deleted": True}
