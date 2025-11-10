from app.components.user.rules import UserPasswordRules


class PasswordPolicies:
    def __init__(self):
        pass

    def get_password_rules(self) -> UserPasswordRules:
        return UserPasswordRules(
            min_length=8,
            max_length=64,
            require_uppercase=True,
            require_special=True,
            require_numeric=True,
        )
