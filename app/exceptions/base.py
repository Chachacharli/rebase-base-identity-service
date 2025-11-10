from fastapi import status

from .exception_codes import ExceptionCode


class AppException(Exception):
    def __init__(
        self,
        message: str,
        code: ExceptionCode = None,
        details: dict = None,
        http_status: int = status.HTTP_400_BAD_REQUEST,
    ):
        self.message = message
        self.code = code
        self.details = details
        self.http_status = http_status
