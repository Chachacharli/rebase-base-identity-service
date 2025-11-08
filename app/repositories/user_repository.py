from sqlmodel import Session, select

from app.exceptions.http_exceptions import NotFoundException
from app.models.role import Role
from app.models.user import User
from app.schemas.user import UserSetRole


class UserRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_by_username(self, username: str):
        return self.session.exec(select(User).where(User.username == username)).first()

    def get_by_email(self, email: str):
        return self.session.exec(select(User).where(User.email == email)).first()

    def create(self, user: User):
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user

    def set_role(self, role: UserSetRole):
        user = self.session.get(User, role.id)
        if not user:
            raise NotFoundException(entity="User", entity_id=role.id)

        role_instance = self.session.get(Role, role.role_id)
        if not role_instance:
            raise NotFoundException(entity="Role", entity_id=role.role_id)

        if role_instance in user.roles:
            return user

        user.roles.append(role_instance)
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user

    def remove_role(self, role: UserSetRole):
        user = self.session.get(User, role.id)
        if not user:
            raise NotFoundException(entity="User", entity_id=role.id)

        role_instance = self.session.get(Role, role.role_id)
        if not role_instance:
            raise NotFoundException(entity="Role", entity_id=role.role_id)

        if role_instance not in user.roles:
            return user

        user.roles.remove(role_instance)
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user
