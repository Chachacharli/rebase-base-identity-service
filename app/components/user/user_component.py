from app.components.user.rules import UserNameValidator, UserPasswordValidator
from app.core.security.password_hasher import PasswordHasher
from app.exceptions.bussiness_exceptions import (
    EmailAlreadyExistsException,
    UserAccountLockedException,
    UserNameAlreadyExistsException,
)
from app.models.user import User
from app.models.user import User as UserModel
from app.policies.password_policies import PasswordPolicies
from app.policies.username_policies import UserNamePolicies
from app.repositories.user_repository import UserRepository


class UserComponent:
    def __init__(self):
        self.password_validator = UserPasswordValidator(
            PasswordPolicies().get_password_rules()
        )
        self.username_validator = UserNameValidator(
            UserNamePolicies().get_username_rules()
        )

    def create_user(self, username: str, password: str, email: str) -> User:
        # Validate username
        if not self.username_validator.validate(username):
            raise ValueError("Username does not meet the required criteria.")

        # Validate password
        if not self.password_validator.validate(password):
            raise ValueError("Password does not meet the required criteria.")

        password_hash = PasswordHasher()
        hashed_password = password_hash.hash(password)

        return User(
            username=username,
            email=email,
            password=hashed_password,
        )

    def is_user_unique(
        self, username: str, email: str, user_repository: UserRepository
    ) -> bool:
        existing_user_by_username = user_repository.get_by_username(username)
        if existing_user_by_username:
            raise UserNameAlreadyExistsException("Username already exists.")

        existing_user_by_email = user_repository.get_by_email(email)
        if existing_user_by_email:
            raise EmailAlreadyExistsException("Email already exists.")

        return True

    def validate_password(self, password: str) -> bool:
        return self.password_validator.validate(password)

    def passwords_match(self, password: str, confirm_password: str) -> bool:
        return password == confirm_password

    def ensure_login_allowed(self, user: UserModel, max_attempts: int) -> None:
        """Ensure the user is allowed to try to login.

        Raises `UserAccountLockedException` if the user's `login_attempts`
        is greater or equal to `max_attempts`.
        """
        if user is None:
            return

        if (user.login_attempts or 0) >= max_attempts:
            raise UserAccountLockedException()
