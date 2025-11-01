from uuid import UUID

from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.core.db import get_session
from app.repositories.permission_repository import PermissionRepository
from app.schemas.permission import PermissionCreate, PermissionRead, PermissionUpdate

router = APIRouter(prefix="/v1/permissions")


@router.get("/")
def list_permissions(session: Session = Depends(get_session)):
    permission_repo = PermissionRepository(session)
    return permission_repo.get_permissions()


@router.post("/")
def create_permission(
    permission: PermissionCreate, session: Session = Depends(get_session)
):
    permission_repo = PermissionRepository(session)
    db_permission = permission_repo.create(permission)
    return PermissionRead.model_validate(db_permission)


@router.get("/{permission_id}")
def get_permission(permission_id: UUID, session: Session = Depends(get_session)):
    permission_repo = PermissionRepository(session)
    db_permission = permission_repo.get_by_id(permission_id)
    return PermissionRead.model_validate(db_permission)


@router.put("/{permission_id}")
def update_permission(
    permission_id: UUID,
    permission: PermissionUpdate,
    session: Session = Depends(get_session),
):
    permission_repo = PermissionRepository(session)
    db_permission = permission_repo.update(permission_id, permission)
    return PermissionRead.model_validate(db_permission)


@router.delete("/{permission_id}")
def delete_permission(permission_id: UUID):
    # soft delete
    return {"deleted": True}
