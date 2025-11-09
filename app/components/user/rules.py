import re
from dataclasses import dataclass

from app.exceptions.bussiness_exceptions import InvalidPasswordException


@dataclass
class UserPasswordRules:
    min_length: int
    max_length: int
    require_uppercase: bool
    require_special: bool
    require_numeric: bool


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
