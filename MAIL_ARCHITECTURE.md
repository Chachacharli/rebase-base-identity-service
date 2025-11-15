# Mail Service Refactoring Guide

## Overview

The mail service has been refactored to follow **SOLID principles** and enable **easy integration of multiple email providers**. This architecture uses the **Strategy Pattern** and **Protocol-based dependency injection** to allow developers to swap email providers without modifying application logic.

## Architecture

### 1. **EmailProvider Protocol** (`mail_component.py`)

The `EmailProvider` protocol defines the interface that all email providers must implement:

```python
class EmailProvider(Protocol):
    """Protocol defining the interface for email providers."""
    
    def send_email(self, to_email: str, subject: str, html_content: str) -> None:
        """Send a single email."""
        ...
    
    def send_bulk_email(
        self, recipients: list[str], subject: str, html_content: str
    ) -> None:
        """Send bulk email to multiple recipients."""
        ...
```

**Benefits:**
- Any service can implement this protocol.
- No tight coupling to specific implementations.
- Easy testing with mock providers.

### 2. **Concrete Implementations**

#### `SMTPEmailProvider` (Default)
Sends emails via standard SMTP servers (Gmail, Office 365, Sendmail, etc.).

```python
from app.components.mail import SMTPEmailProvider

provider = SMTPEmailProvider(mail_settings)
provider.send_email("user@example.com", "Hello", "<h1>Hello</h1>")
```

#### `SendGridEmailProvider` (Template for Third-Party Services)
Skeleton implementation for SendGrid. Developers can extend this for Mailgun, AWS SES, Twilio SendGrid, etc.

```python
from app.components.mail import SendGridEmailProvider

provider = SendGridEmailProvider(api_key="your-sendgrid-key")
provider.send_email("user@example.com", "Hello", "<h1>Hello</h1>")
```

### 3. **MailManager** (`mail_manager.py`)

Orchestrates email sending by:
1. **Rendering templates** using Jinja2.
2. **Building email contexts** (URLs, tokens, etc.).
3. **Delegating to the provider** for actual sending.

```python
from app.components.mail import MailManager, SMTPEmailProvider

provider = SMTPEmailProvider(mail_settings)
manager = MailManager(provider)

# Send predefined emails
manager.send_reset_password_email("user@example.com", "token123")
manager.send_verification_email("user@example.com", "token456")

# Send custom emails
manager.send_custom_email(
    to_email="user@example.com",
    subject="Custom Email",
    template_name="my_custom_template.html",
    context={"user_name": "John", "order_id": "12345"}
)

# Send bulk emails
manager.send_bulk_email(
    recipients=["user1@example.com", "user2@example.com"],
    subject="Newsletter",
    template_name="newsletter.html",
    context={"month": "November"}
)
```

### 4. **MailService** (`services/mail_service.py`)

A high-level service for application-wide email operations. It wraps `MailManager` with a default provider.

```python
from app.services.mail_service import MailService

mail_service = MailService()
mail_service.send_reset_password_email("user@example.com", "token123")
```

### 5. **Rules** (`rules.py`)

Centralized management of email types, URL builders, and constants.

```python
from app.components.mail.rules import EmailType, EmailUrls

# URL builders
reset_url = EmailUrls.reset_password_url("token123")
verify_url = EmailUrls.verification_url("token456")

# Email types (for logging, analytics, etc.)
email_type = EmailType.RESET_PASSWORD
```

## How to Add a New Email Provider

### Example: Adding AWS SES Support

1. **Create a new provider class** in `mail_component.py`:

```python
class AWSSESEmailProvider(EmailProvider):
    """AWS SES-based email provider."""
    
    def __init__(self, region: str = "us-east-1"):
        """Initialize with AWS region."""
        import boto3
        self.client = boto3.client("ses", region_name=region)
        self.from_email = "noreply@example.com"
    
    def send_email(self, to_email: str, subject: str, html_content: str) -> None:
        """Send email via AWS SES."""
        try:
            self.client.send_email(
                Source=self.from_email,
                Destination={"ToAddresses": [to_email]},
                Message={
                    "Subject": {"Data": subject},
                    "Body": {"Html": {"Data": html_content}},
                },
            )
        except Exception as e:
            raise Exception(f"Failed to send email via AWS SES: {e}") from e
    
    def send_bulk_email(
        self, recipients: list[str], subject: str, html_content: str
    ) -> None:
        """Send bulk email via AWS SES."""
        for to_email in recipients:
            self.send_email(to_email, subject, html_content)
```

2. **Export the provider** in `mail/__init__.py`:

```python
from app.components.mail.mail_component import AWSSESEmailProvider

__all__ = [
    "EmailProvider",
    "SMTPEmailProvider",
    "SendGridEmailProvider",
    "AWSSESEmailProvider",  # Add this
    "MailManager",
    "EmailType",
    "EmailUrls",
]
```

3. **Use it in your application**:

```python
from app.components.mail import MailManager, AWSSESEmailProvider

provider = AWSSESEmailProvider(region="eu-west-1")
manager = MailManager(provider)
manager.send_reset_password_email("user@example.com", "token123")
```

## Migration from Old Code

### Before
```python
from app.services.mail_service import MailService

mail_service = MailService()
mail_service.send_reset_password_email("user@example.com", "token")
```

### After (No changes needed!)
The `MailService` maintains the same interface, so existing code works without modification. Behind the scenes, it now uses the refactored architecture.

## Testing with Mock Providers

For unit tests, create a mock provider:

```python
from app.components.mail import EmailProvider

class MockEmailProvider(EmailProvider):
    """Mock provider for testing."""
    
    def __init__(self):
        self.sent_emails = []
    
    def send_email(self, to_email: str, subject: str, html_content: str) -> None:
        self.sent_emails.append({
            "to": to_email,
            "subject": subject,
            "html": html_content,
        })
    
    def send_bulk_email(
        self, recipients: list[str], subject: str, html_content: str
    ) -> None:
        for to_email in recipients:
            self.send_email(to_email, subject, html_content)

# Usage in tests
def test_password_reset():
    mock_provider = MockEmailProvider()
    manager = MailManager(mock_provider)
    
    manager.send_reset_password_email("user@example.com", "token123")
    
    assert len(mock_provider.sent_emails) == 1
    assert mock_provider.sent_emails[0]["to"] == "user@example.com"
    assert "token123" in mock_provider.sent_emails[0]["html"]
```

## Dependency Injection Pattern

For more advanced setups using FastAPI dependency injection:

```python
from fastapi import Depends
from app.components.mail import MailManager, SMTPEmailProvider

def get_mail_manager() -> MailManager:
    """Dependency to inject MailManager."""
    provider = SMTPEmailProvider(mail_settings)
    return MailManager(provider)

@router.post("/password-reset")
async def reset_password(
    email: str,
    token: str,
    mail_manager: MailManager = Depends(get_mail_manager)
):
    """Reset password endpoint using injected mail manager."""
    mail_manager.send_reset_password_email(email, token)
    return {"message": "Password reset email sent"}
```

## Summary

| Layer | Responsibility | Extensibility |
|-------|-----------------|----------------|
| **EmailProvider** | Send emails via specific service (SMTP, SendGrid, AWS SES) | Add new implementations |
| **MailManager** | Template rendering, context building, delegation | Configure providers, add templates |
| **MailService** | Application-level abstraction, default provider | Swap provider via config |
| **Rules** | Email types, URL builders, constants | Add new types or URL patterns |

This refactoring ensures:
- ✅ **Easy provider switching** without code changes
- ✅ **Testability** with mock providers
- ✅ **Maintainability** with clear separation of concerns
- ✅ **Scalability** to support multiple providers simultaneously
- ✅ **Backward compatibility** with existing code
