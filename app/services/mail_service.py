import smtplib
from email.message import EmailMessage
from enum import Enum

from app.core.config import MailSettings, mail_settings, settings


class EmailType(Enum):
    RESET_PASSWORD = "reset_password"
    VERIFICATION = "verification"


class EmailUrls:
    @staticmethod
    def reset_password_url(token: str) -> str:
        return f"{settings.BASE_URL}/reset-password?token={token}"

    @staticmethod
    def verification_url(token: str) -> str:
        return f"{settings.BASE_URL}/verify-email?token={token}"


class MailService:
    def __init__(self, mail_settings: MailSettings = mail_settings):
        self.smtp_server = mail_settings.SMTP_SERVER
        self.smtp_port = mail_settings.SMTP_PORT
        self.smtp_username = mail_settings.SMTP_USERNAME
        self.smtp_password = mail_settings.SMTP_PASSWORD

    def send_email(self, to_email: str, subject: str, html_content: str):
        """Método genérico para enviar correos HTML."""

        msg = EmailMessage()
        msg["Subject"] = subject
        msg["From"] = self.smtp_username
        msg["To"] = to_email
        msg.set_content("Tu cliente de correo no soporta HTML.")
        msg.add_alternative(html_content, subtype="html")

        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.ehlo()
                server.starttls()
                server.login(self.smtp_username, self.smtp_password)
                server.send_message(msg)
        except Exception as e:
            print(f"Error al enviar correo: {e}")
            raise

    def send_reset_password_email(self, to_email: str, token: str):
        link = EmailUrls.reset_password_url(token)

        html = f"""
        <html>
        <body>
            <h2>Recupera tu contraseña</h2>
            <p>Da clic en el siguiente enlace para restablecer tu contraseña:</p>
            <p><a href="{link}">Restablecer contraseña</a></p>
            <p>Si no solicitaste este correo, ignóralo.</p>
        </body>
        </html>
        """

        self.send_email(
            to_email=to_email, subject="Restablecer contraseña", html_content=html
        )

    def send_verification_email(self, to_email: str, token: str):
        link = EmailUrls.verification_url(token)

        html = f"""
        <html>
        <body>
            <h2>Verifica tu correo electrónico</h2>
            <p>Da clic en el enlace para confirmar tu cuenta:</p>
            <p><a href="{link}">Verificar correo</a></p>
        </body>
        </html>
        """

        self.send_email(
            to_email=to_email, subject="Verificación de correo", html_content=html
        )
