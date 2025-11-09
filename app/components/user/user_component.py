from app.components.user.rules import UserPasswordRules, UserPasswordValidator
from app.core.security.password_hasher import PasswordHasher
from app.exceptions.bussiness_exceptions import (
    EmailAlreadyExistsException,
    UserNameAlreadyExistsException,
)
from app.models.user import User
from app.repositories.user_repository import UserRepository

rules = UserPasswordRules(
    min_length=8,
    max_length=64,
    require_uppercase=True,
    require_special=True,
    require_numeric=True,
)


class UserComponent:
    def __init__(self):
        self.password_validator = UserPasswordValidator(rules)

    def create_user(self, username: str, password: str, email: str) -> User:
        # Validate password
        if self.password_validator.validate(password):
            ValueError("Password does not meet the required criteria.")

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
