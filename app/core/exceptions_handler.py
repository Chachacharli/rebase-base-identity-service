from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.exceptions.base import AppException
from app.schemas.error import ErrorResponse


def register_exception_handlers(app: FastAPI):
    @app.exception_handler(AppException)
    async def app_exception_handler(request: Request, exc: AppException):
        error_response = ErrorResponse(
            error=exc.code,
            message=exc.message,
            details=exc.details,
            code=exc.code,
        )
        return JSONResponse(
            status_code=exc.http_status, content=error_response.model_dump()
        )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception):
        error_response = ErrorResponse(
            error="INTERNAL_SERVER_ERROR",
            message=str(exc),
        )
        return JSONResponse(status_code=500, content=error_response.model_dump())
