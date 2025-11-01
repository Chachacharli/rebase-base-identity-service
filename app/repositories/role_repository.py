from uuid import UUID

from sqlalchemy.orm import selectinload
from sqlmodel import Session, select

from app.exceptions.http_exceptions import NotFoundException
from app.models.permission import Permission
from app.models.role import Role
from app.schemas.role import (
    RoleCreate,
    RoleSetPermission,
    RoleUpdate,
)


class RoleRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_roles(self):
        query = select(Role).options(selectinload(Role.permissions))
        return self.session.exec(query).all()

    def get_by_id(self, role_id: UUID):
        query = (
            select(Role)
            .where(Role.id == role_id)
            .options(selectinload(Role.permissions))
        )

        if not self.session.exec(query).first():
            raise NotFoundException(entity="Role", entity_id=role_id)

        return self.session.exec(query).first()

    def create(self, role: RoleCreate):
        db_role = Role.model_validate(role)
        self.session.add(db_role)
        self.session.commit()
        self.session.refresh(db_role)
        return db_role

    def update(self, role_id: UUID, role_update: RoleUpdate):
        role = self.get_by_id(role_id)
        if not role:
            raise NotFoundException(entity="Role", entity_id=role_id)

        role_data = role_update.model_dump(exclude_unset=True)
        for key, value in role_data.items():
            setattr(role, key, value)

        self.session.add(role)
        self.session.commit()
        self.session.refresh(role)
        return role

    def set_permission(self, role_id: UUID, role_set_permission: RoleSetPermission):
        role = self.get_by_id(role_id)
        if not role:
            raise NotFoundException(entity="Role", entity_id=role_id)

        permission = self.session.get(Permission, role_set_permission.permission_id)
        if not permission:
            raise NotFoundException(
                entity="Permission", entity_id=role_set_permission.permission_id
            )

        if permission not in role.permissions:
            role.permissions.append(permission)

        self.session.add(role)
        self.session.commit()
        self.session.refresh(role)
        return role

    def remove_permission(self, role_id: UUID, role_set_permission: RoleSetPermission):
        role = self.get_by_id(role_id)
        if not role:
            raise NotFoundException(entity="Role", entity_id=role_id)

        permission = self.session.get(Permission, role_set_permission.permission_id)
        if not permission:
            raise NotFoundException(
                entity="Permission", entity_id=role_set_permission.permission_id
            )

        if permission in role.permissions:
            role.permissions.remove(permission)

        self.session.add(role)
        self.session.commit()
        self.session.refresh(role)
        return role
