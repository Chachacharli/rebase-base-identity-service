from fastapi import status


class AppException(Exception):
    def __init__(
        self,
        message: str,
        code: str = None,
        details: dict = None,
        http_status: int = status.HTTP_400_BAD_REQUEST,
    ):
        self.message = message
        self.code = code
        self.details = details
        self.http_status = http_status


class NotFoundException(AppException):
    def __init__(self, entity: str, entity_id: str):
        super().__init__(
            message=f"{entity} with ID {entity_id} not found",
            code="NOT_FOUND",
            http_status=status.HTTP_404_NOT_FOUND,
        )


class UnauthorizedException(AppException):
    def __init__(self, message="Unauthorized"):
        super().__init__(
            message=message,
            code="UNAUTHORIZED",
            http_status=status.HTTP_401_UNAUTHORIZED,
        )
