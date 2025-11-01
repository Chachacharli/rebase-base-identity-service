from uuid import UUID

from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.core.db import get_session
from app.repositories.role_repository import RoleRepository
from app.schemas.role import RoleCreate, RoleRead, RoleSetPermission, RoleUpdate

router = APIRouter(prefix="/v1/roles")


@router.get("/")
def list_roles(session: Session = Depends(get_session)) -> list[RoleRead]:
    role_repo = RoleRepository(session)
    roles = role_repo.get_roles()
    return [RoleRead.model_validate(role) for role in roles]


@router.post("/")
def create_role(role: RoleCreate, session: Session = Depends(get_session)):
    role_repo = RoleRepository(session)
    db_role = role_repo.create(role)
    return RoleRead.model_validate(db_role)


@router.get("/{role_id}")
def get_role(role_id: UUID, session: Session = Depends(get_session)):
    role_repo = RoleRepository(session)
    db_role = role_repo.get_by_id(role_id)
    return RoleRead.model_validate(db_role)


@router.put("/{role_id}")
def update_role(
    role_id: UUID, role: RoleUpdate, session: Session = Depends(get_session)
):
    role_repo = RoleRepository(session)
    db_role = role_repo.update(role_id, role)
    return RoleRead.model_validate(db_role)


@router.delete("/{role_id}")
def delete_role(role_id: UUID):
    # soft delete
    return {"deleted": True}


@router.post("/{role_id}/set_permission")
def set_role_permission(
    role_id: UUID,
    role_set_permission: RoleSetPermission,
    session: Session = Depends(get_session),
):
    role_repo = RoleRepository(session)
    db_role = role_repo.set_permission(role_id, role_set_permission)
    return RoleRead.model_validate(db_role)


@router.put("/{role_id}/remove_permission")
def remove_role_permission(
    role_id: UUID,
    role_set_permission: RoleSetPermission,
    session: Session = Depends(get_session),
):
    role_repo = RoleRepository(session)
    db_role = role_repo.remove_permission(role_id, role_set_permission)
    return RoleRead.model_validate(db_role)


@router.get("/test")
def test_error(test: str):
    print("Generating internal error...", test)
    raise ValueError("Esto es una prueba de error interno")
