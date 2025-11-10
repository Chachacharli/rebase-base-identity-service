from uuid import UUID

from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.core.db import get_session
from app.repositories.role_repository import RoleRepository
from app.schemas.role import RoleCreate, RoleRead, RoleSetPermission, RoleUpdate
from app.services.role_service import RoleService

router = APIRouter(prefix="/v1/roles")


@router.get("/")
def list_roles(session: Session = Depends(get_session)) -> list[RoleRead]:
    role_service = RoleService(RoleRepository(session))
    roles = role_service.get_roles()
    return [RoleRead.model_validate(role) for role in roles]


@router.post("/")
def create_role(role: RoleCreate, session: Session = Depends(get_session)):
    role_service = RoleService(RoleRepository(session))
    db_role = role_service.create_role(role)
    return RoleRead.model_validate(db_role)


@router.get("/{role_id}")
def get_role(role_id: UUID, session: Session = Depends(get_session)):
    role_service = RoleService(RoleRepository(session))
    db_role = role_service.get_role(role_id)
    return RoleRead.model_validate(db_role)


@router.put("/{role_id}")
def update_role(
    role_id: UUID, role: RoleUpdate, session: Session = Depends(get_session)
):
    role_service = RoleService(RoleRepository(session))
    db_role = role_service.update_role(role_id, role)
    return RoleRead.model_validate(db_role)


@router.delete("/{role_id}")
def delete_role(role_id: UUID):
    # soft delete
    return {"deleted": True}


@router.post("/set_permission")
def set_role_permission(
    role_set_permission: RoleSetPermission,
    session: Session = Depends(get_session),
):
    role_service = RoleService(RoleRepository(session))
    db_role = role_service.set_permission(
        role_set_permission.role_id, role_set_permission
    )
    return RoleRead.model_validate(db_role)


@router.put("/remove_permission")
def remove_role_permission(
    role_set_permission: RoleSetPermission,
    session: Session = Depends(get_session),
):
    role_service = RoleService(RoleRepository(session))
    db_role = role_service.remove_permission(
        role_set_permission.role_id, role_set_permission
    )
    return RoleRead.model_validate(db_role)
