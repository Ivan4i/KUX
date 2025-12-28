"""Global error handling middleware for FastAPI"""

from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError
from loguru import logger
import traceback
from typing import Union


class AppException(Exception):
    """Base exception for application errors"""

    def __init__(self, message: str, status_code: int = 500, details: dict = None):
        self.message = message
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)


class NotFoundException(AppException):
    """Resource not found exception"""

    def __init__(self, resource: str, identifier: str):
        super().__init__(
            message=f"{resource} not found: {identifier}",
            status_code=status.HTTP_404_NOT_FOUND,
            details={"resource": resource, "identifier": identifier}
        )


class ValidationException(AppException):
    """Validation error exception"""

    def __init__(self, message: str, errors: list = None):
        super().__init__(
            message=message,
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            details={"errors": errors or []}
        )


class DeviceUnavailableException(AppException):
    """Device not available exception"""

    def __init__(self, device_id: str, reason: str = "Device is not available"):
        super().__init__(
            message=f"Device {device_id} unavailable: {reason}",
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            details={"device_id": device_id, "reason": reason}
        )


async def app_exception_handler(request: Request, exc: AppException):
    """Handle custom application exceptions"""
    logger.warning(
        f"AppException: {exc.message} "
        f"(status={exc.status_code}, path={request.url.path})"
    )

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.message,
            "details": exc.details,
            "path": str(request.url.path)
        }
    )


async def validation_exception_handler(
    request: Request,
    exc: Union[RequestValidationError, ValidationError]
):
    """Handle Pydantic validation errors"""
    errors = []

    for error in exc.errors():
        errors.append({
            "field": ".".join(str(x) for x in error["loc"]),
            "message": error["msg"],
            "type": error["type"]
        })

    logger.warning(
        f"Validation error on {request.url.path}: {len(errors)} field(s) failed validation"
    )

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": "Validation failed",
            "details": {"validation_errors": errors},
            "path": str(request.url.path)
        }
    )


async def database_exception_handler(request: Request, exc: SQLAlchemyError):
    """Handle database errors"""
    logger.error(
        f"Database error on {request.url.path}: {str(exc)}",
        exc_info=True
    )

    # Don't expose internal database errors to clients
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "A database error occurred",
            "details": {"message": "Please try again later"},
            "path": str(request.url.path)
        }
    )


async def general_exception_handler(request: Request, exc: Exception):
    """Handle all other uncaught exceptions"""
    # Log full traceback for debugging
    logger.error(
        f"Unhandled exception on {request.url.path}: {str(exc)}",
        exc_info=True
    )

    # Get traceback for internal logging
    tb = traceback.format_exc()
    logger.debug(f"Traceback: {tb}")

    # Return generic error to client (don't expose internals)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "An internal server error occurred",
            "details": {"message": "Please contact support if this persists"},
            "path": str(request.url.path)
        }
    )


def setup_error_handlers(app):
    """Register all error handlers with FastAPI app"""
    app.add_exception_handler(AppException, app_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(ValidationError, validation_exception_handler)
    app.add_exception_handler(SQLAlchemyError, database_exception_handler)
    app.add_exception_handler(Exception, general_exception_handler)

    logger.info("✅ Error handlers registered")
