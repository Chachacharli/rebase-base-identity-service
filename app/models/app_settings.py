from sqlmodel import Field, SQLModel

from app.models.base import AuditMixin, PKMixin, TimestampMixin


class AppSetting(SQLModel, PKMixin, TimestampMixin, AuditMixin, table=True):
    __tablename__ = "app_settings"

    key: str = Field(index=True, unique=True)
    value: str | None = None
    description: str | None = None
    is_active: bool = Field(default=True, index=True)
