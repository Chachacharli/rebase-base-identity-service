import uuid
from datetime import datetime

from sqlmodel import Field, SQLModel

from app.models.base import PKMixin


class RefreshToken(SQLModel, PKMixin, table=True):
    __tablename__ = "refresh_tokens"
    token: str
    user_id: uuid.UUID = Field(foreign_key="user.id")
    client_id: str
    scope: str
    expires_at: datetime
    revoked: bool = False
