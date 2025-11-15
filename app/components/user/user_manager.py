from app.components.user.user_component import UserComponent
from app.core.config import settings
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.services.mail_service import MailService
from app.services.password_service import PasswordService


class UserManager:
    def __init__(self, repository: UserRepository):
        self.user_component = UserComponent()
        self.user_repository = repository
        self.password_service = PasswordService("secret")

    def get_user(self, user_id: int):
        # Logic to retrieve a user by ID
        pass

    def create_user(self, username: str, password: str, email: str) -> User:
        self.user_component.is_user_unique(username, email, self.user_repository)

        new_user = self.user_component.create_user(username, password, email)
        user = self.user_repository.create(new_user)
        self.send_verification_email(email)
        return user

    def send_verification_email(self, email: str):
        mail_service = MailService()
        token = self.password_service.generate_token(email)
        mail_service.send_verification_email(email, token)

    def verify_email(self, token: str) -> bool:
        """Verify an email using a token. Returns True if verification succeeded."""
        user_email = self.password_service.verify_token(token)
        if not user_email:
            return False

        user = self.user_repository.get_by_email(user_email)
        if not user:
            return False

        # Update user as verified
        updated_user = self.user_repository.set_email_verified(user)
        return bool(updated_user)

    def send_mail_reset_password(self, email: str) -> bool:
        token = self.password_service.generate_token(email)
        mail_service = MailService()
        try:
            mail_service.send_reset_password_email(email, token)
            return True
        except Exception as e:
            print(f"Error sending reset password email: {e}")

    def reset_password(self, new_password: str, token: str) -> User:
        user_email = self.password_service.verify_token(token)

        if not user_email:
            raise ValueError("Invalid or expired token.")

        user = self.user_repository.get_by_email(user_email)
        if not user:
            raise ValueError("User not found.")

        self.user_component.validate_password(new_password)

        hashed_password = self.password_service.hash_password(new_password)

        response = self.user_repository.change_password(user, hashed_password)

        return response

    def validate_user_credentials(self, user: User, password: str) -> bool:
        """Validate user's credentials, enforce login attempts lockout and update last_login.

        - If the user is locked due to too many failed attempts, raise UserAccountLockedException.
        - On successful authentication: reset attempts to 0 and set last_login to now.
        - On failed authentication: increment attempts.
        """
        if user is None:
            return False

        # Delegate lock check to UserComponent using configured max attempts
        self.user_component.ensure_login_allowed(user, settings.MAX_LOGIN_ATTEMPTS)

        verified = self.password_service.verify_password(password, user.password)
        if verified:
            # successful login: reset attempts and update last_login
            self.user_repository.reset_login_attempts_and_set_last_login(user)
            return True
        else:
            # failed login: increment attempts
            self.user_repository.increment_login_attempts(user)
            return False
