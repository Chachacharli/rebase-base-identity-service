from typing import TYPE_CHECKING, Optional

from sqlmodel import Column, Field, Relationship, SQLModel, String

from app.models.base import AuditMixin, PKMixin, TimestampMixin
from app.models.role_permission import RolePermission

if TYPE_CHECKING:
    from app.models.role import Role


class Permission(SQLModel, PKMixin, AuditMixin, TimestampMixin, table=True):
    __tablename__ = "permissions"
    name: str = Field(nullable=False)
    description: Optional[str] = Field(default=None)

    roles: list["Role"] = Relationship(
        back_populates="permissions", link_model=RolePermission
    )
