from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel


class UserCreate(BaseModel):
    username: str
    email: str
    password: str


class UserRead(BaseModel):
    id: UUID
    username: str
    email: str

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    username: Optional[str]
    email: Optional[str]
    password: Optional[str]


class UserSetRole(BaseModel):
    id: UUID
    role_id: UUID


class UserSetRoles(BaseModel):
    id: UUID
    role_ids: List[UUID]
