from uuid import UUID

from app.repositories.permission_repository import PermissionRepository
from app.schemas.permission import PermissionCreate, PermissionUpdate


class PermissionService:
    def __init__(self, repository: PermissionRepository):
        self.repository = repository

    def get_permissions(self):
        return self.repository.get_permissions()

    def get_permission(self, permission_id: UUID):
        return self.repository.get_by_id(permission_id)

    def create_permission(self, permission: PermissionCreate):
        return self.repository.create(permission)

    def update_permission(
        self, permission_id: UUID, permission_update: PermissionUpdate
    ):
        return self.repository.update(permission_id, permission_update)
