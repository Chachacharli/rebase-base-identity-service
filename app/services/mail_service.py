"""Mail service layer providing high-level email operations.

This module acts as a thin wrapper around MailManager, providing a dependency
injection point and simplifying integration throughout the application.
"""

from app.components.mail import MailManager, SMTPEmailProvider
from app.core.config import mail_settings


class MailService:
    """High-level mail service for sending emails across the application.

    This service initializes MailManager with a default SMTP provider but can be
    easily modified to support different providers or configurations.

    Usage:
        mail_service = MailService()
        mail_service.send_reset_password_email("user@example.com", "token123")
    """

    def __init__(self):
        """Initialize mail service with default SMTP provider."""
        self.provider = SMTPEmailProvider(mail_settings)
        self.manager = MailManager(self.provider)

    def send_reset_password_email(self, to_email: str, token: str) -> None:
        self.manager.send_reset_password_email(to_email, token)

    def send_verification_email(self, to_email: str, token: str) -> None:
        self.manager.send_verification_email(to_email, token)

    def send_custom_email(
        self, to_email: str, subject: str, template_name: str, context: dict
    ) -> None:
        """Send a custom email using a template.

        Args:
            to_email: Recipient email address.
            subject: Email subject line.
            template_name: Name of the template file (e.g., "my_template.html").
            context: Dictionary of variables to render in the template.

        Raises:
            Exception: If template not found or email sending fails.
        """
        self.manager.send_custom_email(to_email, subject, template_name, context)

    def send_bulk_email(
        self,
        recipients: list[str],
        subject: str,
        template_name: str,
        context: dict,
    ) -> None:
        """Send bulk email to multiple recipients.

        Args:
            recipients: List of recipient email addresses.
            subject: Email subject line.
            template_name: Name of the template file.
            context: Dictionary of variables to render in the template.

        Raises:
            Exception: If template not found or email sending fails.
        """
        self.manager.send_bulk_email(recipients, subject, template_name, context)
