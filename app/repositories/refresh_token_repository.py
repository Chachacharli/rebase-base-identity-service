from sqlmodel import Session, select

from app.models.refresh_token import RefreshToken


class RefreshTokenRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, token: RefreshToken) -> RefreshToken:
        self.session.add(token)
        self.session.commit()
        self.session.refresh(token)
        return token

    def get(self, token_str: str) -> RefreshToken | None:
        return self.session.exec(
            select(RefreshToken).where(RefreshToken.token == token_str)
        ).first()

    def revoke(self, token_str: str) -> RefreshToken:
        token = self.get(token_str)
        if token:
            token.revoked = True
            self.session.add(token)
            self.session.commit()
        return token

    def mark_replaced(self, old: RefreshToken, new: RefreshToken) -> None:
        old.revoked = True
        old.replaced_by = new.id
        new.parent_id = old.id
        self.session.add_all([old, new])

    def revoke_chain(self, refresh_token: RefreshToken) -> None:
        """Revoke token and its descendants (recursivo / iterativo)."""
        stack = [refresh_token]
        while stack:
            r = stack.pop()
            r.revoked = True
            self.session.add(r)
            # buscar hijos directos (tokens que tienen parent_id == r.id)
            q = (
                select(RefreshToken)
                .where(RefreshToken.parent_id == r.id)
                .where(not RefreshToken.revoked)
            )
            children = self.session.exec(q).all()
            stack.extend(children)
