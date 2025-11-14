"""Mail component module for sending emails with pluggable providers.

This module provides a clean, extensible architecture for email sending:
- EmailProvider: Protocol defining the interface for email providers.
- SMTPEmailProvider: Default SMTP-based implementation.
- SendGridEmailProvider: Example third-party provider (template).
- MailManager: Orchestrates email sending with template rendering.
- Rules: Email types and URL builders.

Usage example:
    from app.components.mail import MailManager, SMTPEmailProvider

    # Initialize with SMTP provider
    provider = SMTPEmailProvider()
    mail_manager = MailManager(provider)

    # Send password reset email
    mail_manager.send_reset_password_email("user@example.com", "token123")

    # Or use with a different provider
    from app.components.mail import SendGridEmailProvider
    sg_provider = SendGridEmailProvider(api_key="your-key")
    mail_manager = MailManager(sg_provider)
    mail_manager.send_reset_password_email("user@example.com", "token123")
"""

from app.components.mail.mail_component import (
    EmailProvider,
    SMTPEmailProvider,
    SendGridEmailProvider,
)
from app.components.mail.mail_manager import MailManager
from app.components.mail.rules import EmailType, EmailUrls

__all__ = [
    "EmailProvider",
    "SMTPEmailProvider",
    "SendGridEmailProvider",
    "MailManager",
    "EmailType",
    "EmailUrls",
]
