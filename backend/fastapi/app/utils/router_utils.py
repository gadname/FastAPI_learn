"""
Shared utilities for FastAPI routers.
Provides common error handling patterns and decorators.
"""

from functools import wraps
from typing import Any, Callable, TypeVar, Dict, Type
from fastapi import HTTPException
from app.utils.logging import logger

F = TypeVar("F", bound=Callable[..., Any])


class RouterException(Exception):
    """Base exception for router-related errors."""

    pass


class ResourceNotFoundError(RouterException):
    """Exception raised when a requested resource is not found."""

    pass


class ResourceCreationError(RouterException):
    """Exception raised when resource creation fails."""

    pass


# Common error mappings
ERROR_MAPPINGS: Dict[Type[Exception], tuple[int, str]] = {
    ValueError: (404, "Resource not found"),
    ResourceNotFoundError: (404, "Resource not found"),
    ResourceCreationError: (500, "Failed to create resource"),
}


def handle_router_exceptions(resource_name: str = "resource") -> Callable[[F], F]:
    """
    Decorator to handle common router exceptions.

    Args:
        resource_name: Name of the resource for logging (e.g., "猫", "ボット")

    Returns:
        Decorated function with exception handling
    """

    def decorator(func: F) -> F:
        @wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except ValueError as e:
                logger.error(f"{resource_name}が見つかりません: {str(e)}")
                raise HTTPException(status_code=404, detail=str(e))
            except ResourceNotFoundError as e:
                logger.error(f"{resource_name}が見つかりません: {str(e)}")
                raise HTTPException(status_code=404, detail=str(e))
            except ResourceCreationError as e:
                logger.error(f"{resource_name}作成エラー: {str(e)}")
                raise HTTPException(status_code=500, detail=str(e))
            except Exception as e:
                logger.error(f"{resource_name}操作エラー: {str(e)}")
                raise HTTPException(status_code=500, detail=str(e))

        return wrapper

    return decorator


def handle_get_operation(resource_name: str = "resource") -> Callable[[F], F]:
    """Decorator specifically for GET operations."""

    def decorator(func: F) -> F:
        @wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except ValueError as e:
                logger.error(f"{resource_name}が見つかりません: {str(e)}")
                raise HTTPException(status_code=404, detail=str(e))
            except Exception as e:
                logger.error(f"{resource_name}取得エラー: {str(e)}")
                raise HTTPException(status_code=500, detail=str(e))

        return wrapper

    return decorator


def handle_create_operation(resource_name: str = "resource") -> Callable[[F], F]:
    """Decorator specifically for CREATE operations."""

    def decorator(func: F) -> F:
        @wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                logger.error(f"{resource_name}作成エラー: {str(e)}")
                raise HTTPException(status_code=500, detail=str(e))

        return wrapper

    return decorator


def handle_update_operation(resource_name: str = "resource") -> Callable[[F], F]:
    """Decorator specifically for UPDATE operations."""

    def decorator(func: F) -> F:
        @wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except ValueError as e:
                logger.error(f"{resource_name}が見つかりません: {str(e)}")
                raise HTTPException(status_code=404, detail=str(e))
            except Exception as e:
                logger.error(f"{resource_name}更新エラー: {str(e)}")
                raise HTTPException(status_code=500, detail=str(e))

        return wrapper

    return decorator


def handle_delete_operation(resource_name: str = "resource") -> Callable[[F], F]:
    """Decorator specifically for DELETE operations."""

    def decorator(func: F) -> F:
        @wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except ValueError as e:
                logger.error(f"{resource_name}が見つかりません: {str(e)}")
                raise HTTPException(status_code=404, detail=str(e))
            except Exception as e:
                logger.error(f"{resource_name}削除エラー: {str(e)}")
                raise HTTPException(status_code=500, detail=str(e))

        return wrapper

    return decorator
