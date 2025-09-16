from typing import List, Optional

from sqlalchemy.dialects.postgresql import JSON
from sqlmodel import Column, Field, SQLModel

from app.models.base import AuditMixin, PKMixin, TimestampMixin


# ---------------------------
# Modelo Client
# ---------------------------
class ClientApplication(SQLModel, PKMixin, TimestampMixin, AuditMixin, table=True):
    __tablename__ = "client_applications"

    client_id: str = Field(index=True, unique=True, nullable=False)
    client_secret: Optional[str] = Field(default=None)
    display_name: str = Field(unique=True, nullable=False)

    redirect_uris: List[str] = Field(sa_column=Column(JSON, nullable=False))

    post_logout_redirect_uris: Optional[List[str]] = Field(
        sa_column=Column(JSON), default=[]
    )

    scopes: List[str] = Field(
        sa_column=Column(JSON), default=["openid", "profile", "email"]
    )

    grant_types: List[str] = Field(
        sa_column=Column(JSON), default=["authorization_code"]
    )

    is_public: bool = Field(default=True)

    tenant_id: Optional[str] = Field(default=None, index=True)
