"""Mail manager orchestrating email sending with pluggable providers."""

from jinja2 import Environment, FileSystemLoader

from app.components.mail.mail_component import EmailProvider
from app.components.mail.rules import EmailUrls


class MailManager:
    """Manages email sending with a configurable provider.

    This class acts as an orchestrator that:
    1. Handles template rendering.
    2. Builds email links and contexts.
    3. Delegates actual sending to the plugged-in provider.

    Developers can easily swap providers by passing a different EmailProvider.
    """

    def __init__(self, email_provider: EmailProvider):
        """Initialize mail manager with a specific email provider.

        Args:
            email_provider: An EmailProvider instance (SMTP, SendGrid, etc.).
        """
        self.provider = email_provider
        self.template_env = Environment(
            loader=FileSystemLoader("app/templates/emails"), autoescape=True
        )

    def send_reset_password_email(self, to_email: str, token: str) -> None:
        """Send a password reset email.

        Args:
            to_email: Recipient email address.
            token: Password reset token.

        Raises:
            Exception: If email sending fails.
        """
        link = EmailUrls.reset_password_url(token)
        html = self.template_env.get_template("reset_password.html").render(link=link)
        self.provider.send_email(
            to_email=to_email, subject="Password Recovery", html_content=html
        )

    def send_verification_email(self, to_email: str, token: str) -> None:
        """Send an email verification email.

        Args:
            to_email: Recipient email address.
            token: Email verification token.

        Raises:
            Exception: If email sending fails.
        """
        link = EmailUrls.verification_url(token)
        html = self.template_env.get_template("verify_email.html").render(link=link)
        self.provider.send_email(
            to_email=to_email, subject="Email Verification", html_content=html
        )

    def send_custom_email(
        self, to_email: str, subject: str, template_name: str, context: dict
    ) -> None:
        """Send a custom email using a template with arbitrary context.

        This method allows flexibility to send other types of emails without
        modifying MailManager.

        Args:
            to_email: Recipient email address.
            subject: Email subject line.
            template_name: Name of the template file (e.g., "my_template.html").
            context: Dictionary of variables to render in the template.

        Raises:
            Exception: If template not found or email sending fails.
        """
        html = self.template_env.get_template(template_name).render(**context)
        self.provider.send_email(to_email=to_email, subject=subject, html_content=html)

    def send_bulk_email(
        self,
        recipients: list[str],
        subject: str,
        template_name: str,
        context: dict,
    ) -> None:
        """Send bulk email to multiple recipients using a template.

        Args:
            recipients: List of recipient email addresses.
            subject: Email subject line.
            template_name: Name of the template file.
            context: Dictionary of variables to render in the template.

        Raises:
            Exception: If template not found or email sending fails.
        """
        html = self.template_env.get_template(template_name).render(**context)
        self.provider.send_bulk_email(
            recipients=recipients, subject=subject, html_content=html
        )
