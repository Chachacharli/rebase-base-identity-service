"""Abstract email provider interface and concrete implementations."""

import smtplib
from email.message import EmailMessage
from typing import Protocol

from app.core.config import MailSettings, mail_settings


class EmailProvider(Protocol):
    """Protocol defining the interface for email providers.

    Any email provider (SMTP, SendGrid, AWS SES, etc.) must implement these methods.
    This allows easy extension without modifying existing code.
    """

    def send_email(self, to_email: str, subject: str, html_content: str) -> None:
        """Send a single email with HTML content.

        Args:
            to_email: Recipient email address.
            subject: Email subject line.
            html_content: HTML body content.

        Raises:
            Exception: If email delivery fails.
        """
        ...

    def send_bulk_email(
        self, recipients: list[str], subject: str, html_content: str
    ) -> None:
        """Send bulk email to multiple recipients (optional optimization).

        Args:
            recipients: List of recipient email addresses.
            subject: Email subject line.
            html_content: HTML body content.

        Raises:
            Exception: If email delivery fails.
        """
        ...


class SMTPEmailProvider(EmailProvider):
    """SMTP-based email provider for sending emails via standard SMTP servers.

    This is the default provider for simple configurations (Gmail, Office 365, etc.).
    """

    def __init__(self, mail_settings: MailSettings = mail_settings):
        """Initialize SMTP provider with configuration.

        Args:
            mail_settings: Mail configuration containing SMTP credentials.
        """
        self.smtp_server = mail_settings.SMTP_SERVER
        self.smtp_port = mail_settings.SMTP_PORT
        self.smtp_username = mail_settings.SMTP_USERNAME
        self.smtp_password = mail_settings.SMTP_PASSWORD
        self.from_email = mail_settings.SMTP_USERNAME

    def send_email(self, to_email: str, subject: str, html_content: str) -> None:
        """Send email via SMTP.

        Args:
            to_email: Recipient email address.
            subject: Email subject line.
            html_content: HTML body content.

        Raises:
            smtplib.SMTPException: If SMTP connection or sending fails.
        """
        msg = EmailMessage()
        msg["Subject"] = subject
        msg["From"] = self.from_email
        msg["To"] = to_email
        msg.set_content("Your email client does not support HTML.")
        msg.add_alternative(html_content, subtype="html")

        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.ehlo()
                server.starttls()
                server.login(self.smtp_username, self.smtp_password)
                server.send_message(msg)
        except Exception as e:
            raise Exception(f"Failed to send email via SMTP: {e}") from e

    def send_bulk_email(
        self, recipients: list[str], subject: str, html_content: str
    ) -> None:
        """Send bulk email to multiple recipients via SMTP.

        Args:
            recipients: List of recipient email addresses.
            subject: Email subject line.
            html_content: HTML body content.

        Raises:
            smtplib.SMTPException: If SMTP connection or sending fails.
        """
        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.ehlo()
                server.starttls()
                server.login(self.smtp_username, self.smtp_password)

                for to_email in recipients:
                    msg = EmailMessage()
                    msg["Subject"] = subject
                    msg["From"] = self.from_email
                    msg["To"] = to_email
                    msg.set_content("Your email client does not support HTML.")
                    msg.add_alternative(html_content, subtype="html")
                    server.send_message(msg)
        except Exception as e:
            raise Exception(f"Failed to send bulk email via SMTP: {e}") from e


class SendGridEmailProvider(EmailProvider):
    """SendGrid-based email provider (example of extending to third-party services).

    Uncomment and install `sendgrid` package to use:
    `pip install sendgrid`
    """

    def __init__(self, api_key: str):
        """Initialize SendGrid provider.

        Args:
            api_key: SendGrid API key.
        """
        self.api_key = api_key
        self.from_email = "noreply@example.com"  # Configure via settings if needed
        # from sendgrid import SendGridAPIClient
        # self.client = SendGridAPIClient(api_key)

    def send_email(self, to_email: str, subject: str, html_content: str) -> None:
        """Send email via SendGrid.

        Args:
            to_email: Recipient email address.
            subject: Email subject line.
            html_content: HTML body content.

        Raises:
            Exception: If SendGrid API call fails.
        """
        # from sendgrid.helpers.mail import Mail
        # message = Mail(
        #     from_email=self.from_email,
        #     to_emails=to_email,
        #     subject=subject,
        #     html_content=html_content,
        # )
        # try:
        #     self.client.send(message)
        # except Exception as e:
        #     raise Exception(f"Failed to send email via SendGrid: {e}") from e
        raise NotImplementedError(
            "SendGrid provider requires 'sendgrid' package. Install with: pip install sendgrid"
        )

    def send_bulk_email(
        self, recipients: list[str], subject: str, html_content: str
    ) -> None:
        """Send bulk email via SendGrid.

        Args:
            recipients: List of recipient email addresses.
            subject: Email subject line.
            html_content: HTML body content.

        Raises:
            Exception: If SendGrid API call fails.
        """
        # from sendgrid.helpers.mail import Mail, Personalization
        # message = Mail(
        #     from_email=self.from_email,
        #     subject=subject,
        #     html_content=html_content,
        # )
        # for to_email in recipients:
        #     message.add_to(to_email)
        # try:
        #     self.client.send(message)
        # except Exception as e:
        #     raise Exception(f"Failed to send bulk email via SendGrid: {e}") from e
        raise NotImplementedError(
            "SendGrid provider requires 'sendgrid' package. Install with: pip install sendgrid"
        )
