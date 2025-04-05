from typing import Dict, Any, Optional, Union, List

from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel

from loguru import logger


class ErrorResponse(BaseModel):
    """
    Standard error response model for API errors.
    
    Provides a consistent structure for all error responses in the API,
    ensuring that clients receive uniform error data regardless of
    error source. This model is serialized to JSON in responses.
    """
    
    detail: str  # Primary error message
    status_code: int  # HTTP status code
    errors: Optional[List[Dict[str, Any]]] = None  # Additional error details when available


class AGNDBException(Exception):
    """
    Base exception for all AGN-DB application-specific exceptions.
    
    Acts as the parent class for all custom exceptions in the application.
    Captures status code, detailed message, and optional structured error data
    to provide consistent error handling throughout the API.
    """
    
    def __init__(
        self, 
        detail: str, 
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
        errors: Optional[List[Dict[str, Any]]] = None
    ):
        """
        Initialize AGNDBException with error details.
        
        Args:
            detail: Human-readable error message
            status_code: HTTP status code to return in the response
            errors: Optional list of structured error details for complex validation failures
        """
        self.detail = detail
        self.status_code = status_code
        self.errors = errors
        super().__init__(self.detail)


class NotFoundException(AGNDBException):
    """
    Exception raised when a requested resource is not found.
    
    Used in repository methods and API handlers when a resource with
    a specified ID or criteria doesn't exist. Maps to HTTP 404 responses.
    """
    
    def __init__(
        self, 
        detail: str = "Resource not found", 
        errors: Optional[List[Dict[str, Any]]] = None
    ):
        """
        Initialize NotFoundException with custom message.
        
        Args:
            detail: Specific message about what resource wasn't found
            errors: Optional list of error details
        """
        super().__init__(detail, status.HTTP_404_NOT_FOUND, errors)


class ValidationException(AGNDBException):
    """
    Exception raised for business logic validation errors.
    
    Used for domain-specific validation that goes beyond basic schema validation,
    such as checking relationships between fields or enforcing business rules.
    Maps to HTTP 422 responses.
    """
    
    def __init__(
        self, 
        detail: str = "Validation error", 
        errors: Optional[List[Dict[str, Any]]] = None
    ):
        """
        Initialize ValidationException with error details.
        
        Args:
            detail: Description of what validation failed
            errors: Optional structured details about validation failures
        """
        super().__init__(detail, status.HTTP_422_UNPROCESSABLE_ENTITY, errors)


class DatabaseException(AGNDBException):
    """
    Exception raised for database-related errors.
    
    Used to wrap SQLAlchemy and other database exceptions, providing a clean
    abstraction that doesn't expose internal database details to API clients.
    Maps to HTTP 500 responses.
    """
    
    def __init__(
        self, 
        detail: str = "Database error", 
        errors: Optional[List[Dict[str, Any]]] = None
    ):
        """
        Initialize DatabaseException with error details.
        
        Args:
            detail: Description of the database error
            errors: Optional structured details about the database failure
        """
        super().__init__(detail, status.HTTP_500_INTERNAL_SERVER_ERROR, errors)


# --- Exception handlers ---

async def agndb_exception_handler(request: Request, exc: AGNDBException) -> JSONResponse:
    """
    Global handler for all AGNDBException types.
    
    Processes any application-specific exception and converts it to a consistent
    JSON response format. Logs the error details with appropriate severity.
    
    Args:
        request: FastAPI request object
        exc: Exception instance of AGNDBException or its subclasses
        
    Returns:
        JSONResponse with standardized error format
    """
    logger.error(f"AGNDBException: {exc.detail} ({exc.status_code})")
    if exc.errors:
        logger.error(f"Error details: {exc.errors}")
        
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            detail=exc.detail,
            status_code=exc.status_code,
            errors=exc.errors
        ).model_dump(),
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    """
    Handler for Pydantic validation errors.
    
    Processes schema validation errors from request data and converts them
    to a consistent error response format. Extracts and formats the validation
    error details from Pydantic's error structure.
    
    Args:
        request: FastAPI request object
        exc: RequestValidationError from Pydantic validation
        
    Returns:
        JSONResponse with structured validation error details
    """
    error_details = []
    for error in exc.errors():
        error_details.append({
            "loc": error.get("loc", []),
            "msg": error.get("msg", ""),
            "type": error.get("type", "")
        })
    
    detail = "Validation error"
    logger.error(f"{detail}: {error_details}")
    
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=ErrorResponse(
            detail=detail,
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            errors=error_details
        ).model_dump(),
    )


async def internal_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    Catch-all handler for unhandled exceptions.
    
    Acts as a safety net for any exceptions not explicitly handled elsewhere.
    Logs the full exception traceback and returns a generic error response
    without exposing implementation details to the client.
    
    Args:
        request: FastAPI request object
        exc: Any unhandled Exception
        
    Returns:
        JSONResponse with generic error message
    """
    detail = "Internal server error"
    logger.exception(f"{detail}: {str(exc)}")
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=ErrorResponse(
            detail=detail,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        ).model_dump(),
    )


# Function to register exception handlers with FastAPI app
def register_exception_handlers(app):
    """
    Register all exception handlers with the FastAPI app.
    
    Connects the exception handlers to the FastAPI application instance,
    establishing the error handling chain. Order matters - more specific
    handlers should be registered before generic ones.
    
    Args:
        app: FastAPI application instance
    """
    app.add_exception_handler(AGNDBException, agndb_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(Exception, internal_exception_handler) 