from app.models.role import Role
from app.repositories.role_repository import RoleRepository
from app.schemas.role import (
    RoleCreate,
    RoleSetPermission,
    RoleUpdate,
)


class RoleService:
    def __init__(self, repository: RoleRepository):
        self.repository = repository

    def create_role(self, role: RoleCreate) -> Role:
        return self.repository.create(role)

    def get_role(self, role_id: int) -> Role:
        return self.repository.get_by_id(role_id)

    def get_roles(self) -> list[Role]:
        return self.repository.get_roles()

    def update_role(self, role_id: int, role: RoleUpdate) -> Role:
        return self.repository.update(role_id, role)

    def remove_permission(self, role_id: int, permission: RoleSetPermission) -> Role:
        return self.repository.remove_permission(role_id, permission)

    def set_permission(self, role_id: int, permission: RoleSetPermission) -> Role:
        return self.repository.set_permission(role_id, permission)
