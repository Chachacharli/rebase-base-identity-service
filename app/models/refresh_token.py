from datetime import datetime

from sqlmodel import Field, SQLModel

from app.models.base import PKMixin


class RefreshToken(SQLModel, PKMixin, table=True):
    token: str
    user_id: str = Field(foreign_key="user.id")
    client_id: str
    scope: str
    expires_at: datetime
    revoked: bool = False
