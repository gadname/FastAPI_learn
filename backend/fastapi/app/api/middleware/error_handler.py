from typing import Any, Dict
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from app.utils.logging import logger


class ErrorResponse(BaseModel):
    """Standard error response model"""
    error: str
    message: str
    details: str | None = None


class CustomHTTPException(HTTPException):
    """Custom HTTP exception with additional context"""
    
    def __init__(
        self,
        status_code: int,
        detail: str,
        error_type: str = "APIError",
        context: Dict[str, Any] | None = None
    ):
        super().__init__(status_code=status_code, detail=detail)
        self.error_type = error_type
        self.context = context or {}


class ErrorHandlerMiddleware:
    """Centralized error handling middleware"""
    
    @staticmethod
    def handle_validation_error(exc: ValueError) -> CustomHTTPException:
        """Handle validation errors"""
        logger.error(f"Validation error: {str(exc)}")
        return CustomHTTPException(
            status_code=400,
            detail=str(exc),
            error_type="ValidationError"
        )
    
    @staticmethod
    def handle_not_found_error(exc: ValueError) -> CustomHTTPException:
        """Handle not found errors"""
        logger.error(f"Not found error: {str(exc)}")
        return CustomHTTPException(
            status_code=404,
            detail=str(exc),
            error_type="NotFoundError"
        )
    
    @staticmethod
    def handle_server_error(exc: Exception) -> CustomHTTPException:
        """Handle server errors"""
        logger.error(f"Server error: {str(exc)}")
        return CustomHTTPException(
            status_code=500,
            detail="Internal server error",
            error_type="ServerError",
            context={"original_error": str(exc)}
        )
    
    @staticmethod
    async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
        """Handle HTTP exceptions"""
        error_response = ErrorResponse(
            error=getattr(exc, 'error_type', 'HTTPException'),
            message=str(exc.detail),
            details=getattr(exc, 'context', None)
        )
        
        return JSONResponse(
            status_code=exc.status_code,
            content=error_response.model_dump()
        )
    
    @staticmethod
    async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
        """Handle general exceptions"""
        logger.error(f"Unhandled exception: {str(exc)}")
        
        error_response = ErrorResponse(
            error="InternalError",
            message="An unexpected error occurred",
            details=str(exc)
        )
        
        return JSONResponse(
            status_code=500,
            content=error_response.model_dump()
        )