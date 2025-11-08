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
