from passlib.hash import pbkdf2_sha256
from sqlmodel import Session, select

from app.models.user import User


class UserService:
    def __init__(self, session: Session):
        self.session = session

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
