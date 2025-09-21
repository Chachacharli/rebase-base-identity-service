from typing import Optional

from models.base import AuditMixin, PKMixin, TimestampMixin
from sqlmodel import Field, SQLModel


class User(SQLModel, PKMixin, TimestampMixin, AuditMixin, table=True):
    username: str = Field(index=True, unique=True, nullable=False)
    password: str
    email: Optional[str] = Field(default=None, index=True, unique=True)
    is_active: bool = Field(default=True)
