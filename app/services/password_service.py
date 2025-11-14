from typing import Optional

from itsdangerous import BadSignature, SignatureExpired, URLSafeTimedSerializer

from app.core.security.password_hasher import PasswordHasher


class PasswordService:
    def __init__(self, secret_key: str, salt: str = "password-reset"):
        self.serializer = URLSafeTimedSerializer(secret_key)
        self.salt = salt

    def generate_token(self, email: str) -> str:
        """Generate a token for password reset"""
        return self.serializer.dumps(email, salt=self.salt)

    def verify_token(self, token: str, max_age: int = 3600) -> Optional[str]:
        """Validate a token and return the email if valid"""
        try:
            return self.serializer.loads(token, salt=self.salt, max_age=max_age)
        except (BadSignature, SignatureExpired):
            return None

    def hash_password(self, password: str) -> str:
        """Hash a password using PBKDF2"""
        return PasswordHasher.hash(password)

    def verify_password(self, password: str, hashed: str) -> bool:
        """Verify a password against its hash"""
        return PasswordHasher.verify(password, hashed)
