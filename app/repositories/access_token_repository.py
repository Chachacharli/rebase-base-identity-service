from sqlmodel import Session, select

from app.models.access_token import AccessToken


class AccessTokenRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, **kwargs) -> AccessToken:
        at = AccessToken(**kwargs)
        self.session.add(at)
        return at

    def get(self, token: str) -> AccessToken | None:
        q = select(AccessToken).where(AccessToken.token == token)
        return self.session.exec(q).one_or_none()

    def revoke_by_refresh(self, refresh_id):
        q = select(AccessToken).where(AccessToken.refresh_token_id == refresh_id)
        for at in self.session.exec(q).all():
            at.revoked = True
            self.session.add(at)

    def revoke(self, access_token: AccessToken):
        access_token.revoked = True
        self.session.add(access_token)
