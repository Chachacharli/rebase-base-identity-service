import secrets
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone

from sqlmodel import Session

from app.models.refresh_token import RefreshToken
from app.repositories.access_token_repository import AccessTokenRepository
from app.repositories.app_settings_repository import AppSettingRepository
from app.repositories.refresh_token_repository import RefreshTokenRepository

ACCESS_TTL = timedelta(minutes=30)
REFRESH_TTL = timedelta(days=7)


@dataclass
class TokenPair:
    access_token: str
    refresh_token: str
    expires_in: int

    def to_dict(self):
        return {
            "access_token": self.access_token,
            "refresh_token": self.refresh_token,
            "expires_in": self.expires_in,
        }


class TokenService:
    def __init__(self, session: Session):
        self.session = session
        self.rt_repo = RefreshTokenRepository(session)
        self.at_repo = AccessTokenRepository(session)
        self.app_settings_repo = AppSettingRepository(session)

    def _now(self):
        return datetime.now(timezone.utc)

    def issue_tokens(self, user_id, client_id, scope) -> TokenPair:
        now = self._now()
        access_token = secrets.token_urlsafe(32)
        refresh_token = secrets.token_urlsafe(48)

        ttl_access = self.app_settings_repo.get("ttl_access_token", 1800)

        # Access token
        self.at_repo.create(
            token=access_token,
            user_id=user_id,
            client_id=client_id,
            scope=scope,
            expires_at=now + ACCESS_TTL,
        )

        rt = RefreshToken(
            token=refresh_token,
            user_id=user_id,
            client_id=client_id,
            scope=scope,
            expires_at=now + REFRESH_TTL,
            revoked=False,
        )

        # Refresh token
        self.rt_repo.create(rt)

        return TokenPair(
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=int(ACCESS_TTL.total_seconds()),
        )

    def refresh_with_rotation(
        self, refresh_token_str: str, client_id: str
    ) -> TokenPair:
        """Usa refresh token para emitir nuevo access + rotar refresh token.
        Detecta reuse si refresh token ya fue revocado.
        """
        now = self._now()
        rt = self.rt_repo.get(refresh_token_str)

        ttl_access = self.app_settings_repo.get("ttl_access_token", 1800)

        if not rt:
            # token desconocido -> posible reuse o ataque: no devolver detalle
            raise ValueError("invalid_grant")

        # Si el refresh token está revocado -> reuse detection
        if rt.revoked:
            # reutilización detectada: revocar cadena completa asociada a este lineage
            self.rt_repo.revoke_chain(rt)
            # revocar accesos derivados
            self.at_repo.revoke_by_refresh(rt.id)
            raise ValueError("Token revoked")

        # Si expiró
        if rt.expires_at < now:
            raise ValueError("Token expired")

        # Validar que el client_id coincide
        if str(rt.client_id) != str(client_id):
            raise ValueError("Invalid client")

        # ROTACIÓN: crear nuevo refresh token y marcar reemplazo
        new_refresh_token_str = secrets.token_urlsafe(48)
        new_rt = self.rt_repo.create(
            token=new_refresh_token_str,
            user_id=rt.user_id,
            client_id=rt.client_id,
            scope=rt.scope,
            expires_at=now + REFRESH_TTL,
        )
        # crear nuevo access token ligado al new_rt
        new_access_token_str = secrets.token_urlsafe(32)
        self.at_repo.create(
            token=new_access_token_str,
            user_id=rt.user_id,
            client_id=rt.client_id,
            scope=rt.scope,
            expires_at=now + ACCESS_TTL,
            refresh_token_id=new_rt.id,
        )

        # Marcar el antiguo como reemplazado (revocar)
        self.rt_repo.mark_replaced(rt, new_rt)

        return TokenPair(
            access_token=new_access_token_str,
            refresh_token=new_refresh_token_str,
            expires_in=int(ACCESS_TTL.total_seconds()),
        )

    def revoke_token(self, token_str: str):
        """Revoke token opaco (access o refresh)."""
        at = self.at_repo.get(token_str)
        if at:
            self.at_repo.revoke(at)
            return

        rt = self.rt_repo.get(token_str)
        if rt:
            # revocar cadena (refresh y descendientes) y sus access tokens
            self.rt_repo.revoke_chain(rt)
            self.at_repo.revoke_by_refresh(rt.id)
            return

        # token desconocido -> ok (es idempotente según RFC)
        return
