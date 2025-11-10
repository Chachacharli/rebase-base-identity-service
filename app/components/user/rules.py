import re
from dataclasses import dataclass

from app.exceptions.bussiness_exceptions import (
    InvalidPasswordException,
    InvalidUsernameException,
)


@dataclass
class UserPasswordRules:
    min_length: int
    max_length: int
    require_uppercase: bool
    require_special: bool
    require_numeric: bool


@dataclass
class UserNameRules:
    min_length: int
    max_length: int
    allow_special_characters: bool
    allow_characters: list[str]


class UserPasswordValidator:
    def __init__(self, rules: UserPasswordRules):
        self.rules = rules

    def validate(self, password: str) -> bool:
        missing_requirements = {}

        if len(password) < self.rules.min_length:
            missing_requirements["min_length"] = (
                f"Password must be at least {self.rules.min_length} characters long."
            )
        if (
            hasattr(self.rules, "require_numeric")
            and self.rules.require_numeric
            and not re.search(r"\d", password)
        ):
            missing_requirements["require_numeric"] = (
                "Password must contain at least one number."
            )
        if self.rules.require_special and not re.search(
            r"[!@#$%^&*(),.?\":{}|<>]", password
        ):
            missing_requirements["require_special"] = (
                "Password must contain a special character."
            )
        if self.rules.require_uppercase and not re.search(r"[A-Z]", password):
            missing_requirements["require_uppercase"] = (
                "Password must contain an uppercase letter."
            )

        if missing_requirements:
            raise InvalidPasswordException(details=missing_requirements)
        return True


class UserNameValidator:
    def __init__(self, rules: UserNameRules):
        self.rules = rules

    def validate(self, username: str) -> bool:
        missing_requirements = {}

        if len(username) < self.rules.min_length:
            missing_requirements["min_length"] = (
                f"Username must be at least {self.rules.min_length} characters long."
            )
        if len(username) > self.rules.max_length:
            missing_requirements["max_length"] = (
                f"Username must be at most {self.rules.max_length} characters long."
            )

        if self.rules.allow_special_characters:
            escaped_chars = "".join(re.escape(c) for c in self.rules.allow_characters)
            pattern = f"^[a-zA-Z0-9{escaped_chars}]+$"
            if not re.match(pattern, username):
                missing_requirements["allow_special_characters"] = (
                    f"Username contains invalid characters. "
                    f"Allowed specials: {''.join(self.rules.allow_characters) or 'none'}"
                )

        if missing_requirements:
            raise InvalidUsernameException(details=missing_requirements)
        return True
