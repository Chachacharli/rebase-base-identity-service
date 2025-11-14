"""Email type definitions and URL builders for email templates."""

from enum import Enum

from app.core.config import settings


class EmailType(Enum):
    """Enumeration of supported email types."""

    RESET_PASSWORD = "reset_password"
    VERIFICATION = "verification"


class EmailUrls:
    """URL builder for email links and callback URLs."""

    @staticmethod
    def reset_password_url(token: str) -> str:
        """Generate reset password link."""
        return f"{settings.BASE_URL}/reset-password?token={token}"

    @staticmethod
    def verification_url(token: str) -> str:
        """Generate email verification link."""
        return f"{settings.BASE_URL}/verify-email?token={token}"
