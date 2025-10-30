from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional
from uuid import UUID


@dataclass
class AuthorizationCode:
    code: str
    client_id: str
    redirect_uri: str
    code_challenge: str
    user_id: UUID
    expires_at: datetime
    scope: List[str] = field(default_factory=lambda: ["openid email profile"])

    @property
    def is_expired(self) -> bool:
        """Verifica si el código ha expirado."""
        return datetime.utcnow() > self.expires_at


class AuthorizationCodeStore:
    """
    Almacén en memoria para los códigos de autorización.
    Puede reemplazarse fácilmente por una implementación persistente (Redis, DB, etc.)
    """

    def __init__(self):
        self._store: Dict[str, AuthorizationCode] = {}

    def save(
        self,
        code: str,
        client_id: str,
        redirect_uri: str,
        code_challenge: str,
        user_id: UUID,
        scope: Optional[List[str]] = None,
        expires_at: Optional[datetime] = None,
    ) -> AuthorizationCode:
        """Guarda un nuevo código de autorización."""
        auth_code = AuthorizationCode(
            code=code,
            client_id=client_id,
            redirect_uri=redirect_uri,
            code_challenge=code_challenge,
            user_id=user_id,
            scope=scope or ["openid"],
            expires_at=expires_at,
        )
        self._store[code] = auth_code
        return auth_code

    def validate(self, code: str) -> Optional[AuthorizationCode]:
        """Valida un código y lo elimina si es válido o expiró."""
        auth_code = self._store.get(code)
        if not auth_code:
            return None

        if auth_code.is_expired:
            del self._store[code]
            return None

        # Código válido, eliminar tras el uso (como exige OAuth2)
        del self._store[code]
        return auth_code


# Instancia global (en memoria)
authorization_code_store = AuthorizationCodeStore()
