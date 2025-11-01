from passlib.hash import pbkdf2_sha256
from sqlalchemy.orm import selectinload
from sqlmodel import Session, select

from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserSetRole


class UserService:
    def __init__(self, session: Session):
        self.session = session

    def get_all_users(self) -> list[User]:
        # TODO: Pagination
        statement = select(User)
        users = self.session.exec(statement).all()
        return users

    def create_user(self, username: str, email: str, password: str) -> User:
        hashed_pw = pbkdf2_sha256.hash(password)
        user = User(username=username, email=email, password=hashed_pw)
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user

    def authenticate_user(self, username: str, password: str) -> User | None:
        statement = select(User).where(User.username == username)
        user = self.session.exec(statement).first()
        if user and pbkdf2_sha256.verify(password, user.password):
            return user
        return None

    def reset_password(self, user: User, new_password: str) -> None:
        hashed_pw = pbkdf2_sha256.hash(new_password)
        user.password = hashed_pw
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)

    def get_user_by_id(self, user_id: str) -> User | None:
        query = select(User).where(User.id == user_id).options(selectinload(User.roles))
        return self.session.exec(query).first()

    def set_user_role(self, user_id: str, role_id: str) -> User | None:
        user_repo = UserRepository(self.session)
        user_set_role = UserSetRole(id=user_id, role_id=role_id)
        updated_user = user_repo.set_role(user_set_role)
        return updated_user
