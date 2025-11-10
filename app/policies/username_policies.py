from app.components.user.rules import UserNameRules


class UserNamePolicies:
    def __init__(self):
        pass

    def get_username_rules(self):
        return UserNameRules(
            min_length=3,
            max_length=30,
            allow_special_characters=True,
            allow_characters=["_-."],
        )
