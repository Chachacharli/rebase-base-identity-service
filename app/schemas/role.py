from typing import Optional
from uuid import UUID

from pydantic import BaseModel

from app.schemas.permission import PermissionRead


class RoleCreate(BaseModel):
    name: str
    description: str


class RoleRead(BaseModel):
    id: UUID
    name: str
    description: str
    permissions: list[PermissionRead] = []

    class Config:
        from_attributes = True


class RoleReadWithoutPermissions(BaseModel):
    id: UUID
    name: str
    description: str

    class Config:
        from_attributes = True


class RoleUpdate(BaseModel):
    name: Optional[str]
    description: Optional[str]


class RoleSetPermission(BaseModel):
    id: UUID
    permission_id: UUID


class RoleSetPermissions(BaseModel):
    id: UUID
    permission_ids: list[UUID]
