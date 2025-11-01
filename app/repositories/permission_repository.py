from sqlmodel import Session, select

from app.models.permission import Permission
from app.schemas.permission import PermissionCreate, PermissionRead, PermissionUpdate


class PermissionRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_permissions(self):
        statement = select(Permission)
        return self.session.exec(statement).all()

    def get_by_id(self, permission_id: str):
        return self.session.exec(
            select(Permission).where(Permission.id == permission_id)
        ).first()

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
