from typing import TYPE_CHECKING, List, Optional

from sqlmodel import Column, Field, Relationship, SQLModel, String

from app.models.base import AuditMixin, PKMixin, TimestampMixin
from app.models.role_permission import RolePermission
from app.models.user_role import UserRole

if TYPE_CHECKING:
    from app.models.permission import Permission
    from app.models.user import User


class Role(SQLModel, PKMixin, AuditMixin, TimestampMixin, table=True):
    __tablename__ = "roles"
    name: str = Field(sa_column=Column(String(100), unique=True))
    description: Optional[str] = Field(default=None)

    # relationships
    users: List["User"] = Relationship(back_populates="roles", link_model=UserRole)  # type: ignore # noqa: F821
    permissions: List["Permission"] = Relationship(
        back_populates="roles", link_model=RolePermission
    )
