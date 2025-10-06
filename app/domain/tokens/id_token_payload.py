import datetime
from dataclasses import dataclass


@dataclass
class IDTokenPayload:
    """Data class representing the payload of an ID token."""

    iss: str
    sub: str
    aud: str
    exp: datetime
    iat: datetime

    def to_dict(self) -> dict:
        """Converts the dataclass to a dictionary suitable for JWT encoding."""
        return {
            "iss": self.iss,
            "sub": self.sub,
            "aud": self.aud,
            "exp": int(self.exp.timestamp()),
            "iat": int(self.iat.timestamp()),
        }
