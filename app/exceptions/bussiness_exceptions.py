from fastapi import status

from .base import AppException
from .exception_codes import ExceptionCode


class TokenExpiredException(AppException):
    def __init__(self, message="Token expired", details=None):
        super().__init__(
            message=message,
            code=ExceptionCode.UNAUTHORIZED,
            http_status=status.HTTP_400_BAD_REQUEST,
            details=details,
        )


class InvalidPasswordException(AppException):
    def __init__(self, message="Invalid password", details=None):
        super().__init__(
            message=message,
            code=ExceptionCode.INVALID_PASSWORD,
            http_status=status.HTTP_400_BAD_REQUEST,
            details=details,
        )


class UserNameAlreadyExistsException(AppException):
    def __init__(self, message="Username already exists", details=None):
        super().__init__(
            message=message,
            code=ExceptionCode.USERNAME_ALREADY_EXISTS,
            http_status=status.HTTP_400_BAD_REQUEST,
            details=details,
        )


class EmailAlreadyExistsException(AppException):
    def __init__(self, message="Email already exists", details=None):
        super().__init__(
            message=message,
            code=ExceptionCode.EMAIL_ALREADY_EXISTS,
            http_status=status.HTTP_400_BAD_REQUEST,
            details=details,
        )


class InvalidUsernameException(AppException):
    def __init__(self, message="Invalid username", details=None):
        super().__init__(
            message=message,
            code=ExceptionCode.VALIDATION_ERROR,
            http_status=status.HTTP_400_BAD_REQUEST,
            details=details,
        )
