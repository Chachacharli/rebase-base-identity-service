from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class PermissionCreate(BaseModel):
    name: str
    description: str


class PermissionRead(BaseModel):
    id: UUID
    name: str
    description: str

    class Config:
        from_attributes = True


class PermissionUpdate(BaseModel):
    name: Optional[str]
    description: Optional[str]
