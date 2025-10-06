from dataclasses import dataclass


@dataclass(frozen=True)
class GrantTokenResponse:
    access_token: str
    token_type: str
    expires_in: int
    id_token: str
    refresh_token: str
    scope: str
    user_id: str
    client_id: str

    def to_dict(self) -> dict:
        return {
            "access_token": self.access_token,
            "token_type": self.token_type,
            "expires_in": self.expires_in,
            "id_token": self.id_token,
            "refresh_token": self.refresh_token,
            "scope": self.scope,
            "user_id": self.user_id,
            "client_id": self.client_id,
        }
