from datetime import datetime
from uuid import UUID

from sqlmodel import Field, SQLModel


class UserRole(SQLModel, table=True):
    __tablename__ = "user_roles"
    user_id: UUID = Field(foreign_key="users.id", primary_key=True)
    role_id: UUID = Field(foreign_key="roles.id", primary_key=True)
    assigned_at: datetime = Field(default_factory=datetime.now, nullable=False)
