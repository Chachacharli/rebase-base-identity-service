from fastapi import status

from .base import AppException
from .exception_codes import ExceptionCode


class UnauthorizedException(AppException):
    def __init__(self, message="Unauthorized", details=None):
        super().__init__(
            message=message,
            code=ExceptionCode.UNAUTHORIZED,
            http_status=status.HTTP_401_UNAUTHORIZED,
            details=details,
        )


class NotFoundException(AppException):
    def __init__(self, entity: str, entity_id: str, details=None):
        super().__init__(
            message=f"{entity} with ID {entity_id} not found",
            code=ExceptionCode.NOT_FOUND,
            http_status=status.HTTP_404_NOT_FOUND,
            details=details,
        )
