from typing import AsyncGenerator, Type, TypeVar, Any
from functools import lru_cache

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from app.db.database import get_db
from app.services.cat import CatService
from app.services.chat_bot import ChatBotService
from app.services.cat_image import CatImageService

# Type variable for service instances
ServiceType = TypeVar("ServiceType")


class ServiceFactory:
    """Factory for creating service instances with proper dependency injection"""
    
    @staticmethod
    @lru_cache(maxsize=None)
    def get_cat_service() -> Type[CatService]:
        """Get CatService instance"""
        return CatService
    
    @staticmethod
    @lru_cache(maxsize=None)
    def get_chat_bot_service() -> Type[ChatBotService]:
        """Get ChatBotService instance"""
        return ChatBotService
    
    @staticmethod
    @lru_cache(maxsize=None)
    def get_cat_image_service() -> CatImageService:
        """Get CatImageService instance"""
        return CatImageService()


# Common dependencies
async def get_database_session() -> AsyncGenerator[AsyncSession, None]:
    """Get database session dependency"""
    async with get_db() as session:
        yield session


# Service dependencies
def get_cat_service_dependency() -> Type[CatService]:
    """Dependency for cat service"""
    return ServiceFactory.get_cat_service()


def get_chat_bot_service_dependency() -> Type[ChatBotService]:
    """Dependency for chat bot service"""
    return ServiceFactory.get_chat_bot_service()


def get_cat_image_service_dependency() -> CatImageService:
    """Dependency for cat image service"""
    return ServiceFactory.get_cat_image_service()


# Database session dependency
database_session = Depends(get_db)