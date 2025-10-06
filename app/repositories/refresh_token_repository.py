from sqlmodel import Session, select

from app.models.refresh_token import RefreshToken


class RefreshTokenRepository:
    def __init__(self, session: Session):
        self.session = session

    def save(self, token: RefreshToken):
        self.session.add(token)
        self.session.commit()
        self.session.refresh(token)
        return token

    def get(self, token_str: str):
        return self.session.exec(
            select(RefreshToken).where(RefreshToken.token == token_str)
        ).first()

    def revoke(self, token_str: str):
        token = self.get(token_str)
        if token:
            token.revoked = True
            self.session.add(token)
            self.session.commit()
        return token
