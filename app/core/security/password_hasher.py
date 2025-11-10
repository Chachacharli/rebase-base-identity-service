from passlib.hash import pbkdf2_sha256


class PasswordHasher:
    @staticmethod
    def hash(password: str) -> str:
        return pbkdf2_sha256.hash(password)

    @staticmethod
    def verify(password: str, hashed: str) -> bool:
        return pbkdf2_sha256.verify(password, hashed)
