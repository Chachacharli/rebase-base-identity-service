from typing import Optional

from sqlmodel import Field, SQLModel

from app.models.base import AuditMixin, PKMixin, TimestampMixin


class User(SQLModel, PKMixin, TimestampMixin, AuditMixin, table=True):
    __tablename__ = "users"
    username: str = Field(index=True, unique=True, nullable=False)
    password: str
    email: Optional[str] = Field(default=None, index=True, unique=True)
    is_active: bool = Field(default=True)
