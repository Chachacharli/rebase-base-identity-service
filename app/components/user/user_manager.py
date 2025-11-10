from app.components.user.user_component import UserComponent
from app.models.user import User
from app.repositories.user_repository import UserRepository


class UserManager:
    def __init__(self, repository: UserRepository):
        self.user_component = UserComponent()
        self.user_repository = repository

    def get_user(self, user_id: int):
        # Logic to retrieve a user by ID
        pass

    def create_user(self, username: str, password: str, email: str) -> User:
        self.user_component.is_user_unique(username, email, self.user_repository)

        new_user = self.user_component.create_user(username, password, email)
        user = self.user_repository.create(new_user)
        return user

    def reset_password(self, user_id: int, new_password: str):
        # Logic to reset a user's password
        pass
