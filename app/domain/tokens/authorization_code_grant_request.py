from dataclasses import dataclass


@dataclass(frozen=True)
class AuthorizationCodeGrantRequest:
    """Data class representing an authorization code grant request."""

    code: str
    redirect_uri: str
    client_id: str
    code_verifier: str
    refresh_token: str = None
    grant_type: str = "authorization_code"

    def to_dict(self) -> dict:
        """Converts the dataclass to a dictionary."""
        return {
            "grant_type": self.grant_type,
            "code": self.code,
            "redirect_uri": self.redirect_uri,
            "client_id": self.client_id,
            "code_verifier": self.code_verifier,
            "refresh_token": self.refresh_token,
        }
