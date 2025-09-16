import uuid
from datetime import datetime
from typing import Optional

from sqlmodel import Field

# ---------------------------
# Mixins Reutilizables
# ---------------------------


class PKMixin:
    """Mixin para ID primario con UUID"""

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)


class TimestampMixin:
    """Mixin para timestamps automáticos"""

    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column_kwargs={"onupdate": datetime.utcnow},
        nullable=False,
    )


class AuditMixin:
    """Mixin para trazabilidad de usuarios"""

    created_by: Optional[str] = Field(default=None)
    updated_by: Optional[str] = Field(default=None)
