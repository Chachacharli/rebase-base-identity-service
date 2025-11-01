from sqlmodel import Session, select

from app.models.permission import Permission
from app.schemas.permission import PermissionCreate, PermissionUpdate

from app.exceptions.base import NotFoundException


class PermissionRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_permissions(self):
        statement = select(Permission)
        return self.session.exec(statement).all()

    def get_by_id(self, permission_id: str):
        permission = self.session.get(Permission, permission_id)
        if not permission:
            raise NotFoundException(entity="Permission", entity_id=permission_id)
        return permission

    def create(self, permission: PermissionCreate):
        permission = Permission.model_validate(permission)
        self.session.add(permission)
        self.session.commit()
        self.session.refresh(permission)
        return permission

    def update(self, permission_id: str, permission_update: PermissionUpdate):
        permission = self.get_by_id(permission_id)
        if not permission:
            return None

        permission_data = permission_update.model_dump(exclude_unset=True)
        for key, value in permission_data.items():
            setattr(permission, key, value)

        self.session.add(permission)
        self.session.commit()
        self.session.refresh(permission)
        return permission
