"""Base service class for unified database operations."""

from abc import ABC, abstractmethod
from typing import Any, Dict, Generic, List, TypeVar

from sqlalchemy.ext.asyncio import AsyncSession

# Type variables for generic service operations
CreateSchemaType = TypeVar("CreateSchemaType")
ResponseSchemaType = TypeVar("ResponseSchemaType")
UpdateSchemaType = TypeVar("UpdateSchemaType")


class BaseService(ABC, Generic[CreateSchemaType, ResponseSchemaType, UpdateSchemaType]):
    """
    Abstract base service class for CRUD operations.
    
    This class provides a common interface for all service classes,
    ensuring consistency across the application.
    """
    
    @staticmethod
    @abstractmethod
    async def create_item(
        db: AsyncSession, 
        item: CreateSchemaType
    ) -> ResponseSchemaType:
        """Create a new item."""
        pass
    
    @staticmethod
    @abstractmethod
    async def get_all_items(db: AsyncSession) -> List[ResponseSchemaType]:
        """Get all items."""
        pass
    
    @staticmethod
    @abstractmethod
    async def get_item_by_id(
        db: AsyncSession, 
        item_id: str
    ) -> ResponseSchemaType:
        """Get item by ID."""
        pass
    
    @staticmethod
    @abstractmethod
    async def update_item(
        item_id: str, 
        item: UpdateSchemaType, 
        db: AsyncSession
    ) -> ResponseSchemaType:
        """Update an item."""
        pass
    
    @staticmethod
    @abstractmethod
    async def delete_item(
        item_id: str, 
        db: AsyncSession
    ) -> Any:
        """Delete an item."""
        pass


class LegacyServiceAdapter:
    """
    Adapter for existing service classes to work with the base router.
    
    This allows existing services to work with the new base router
    without requiring immediate refactoring.
    """
    
    def __init__(self, service_class: Any):
        self.service_class = service_class
    
    async def create_item(self, db: AsyncSession, item: Any) -> Any:
        """Adapt create operation."""
        # Try different method names that might exist
        if hasattr(self.service_class, 'create_chat_bot'):
            return await self.service_class.create_chat_bot(db, item)
        elif hasattr(self.service_class, 'create_cat'):
            return await self.service_class.create_cat(db, item)
        else:
            raise NotImplementedError("Create method not found")
    
    async def get_all_items(self, db: AsyncSession) -> Any:
        """Adapt get all operation."""
        if hasattr(self.service_class, 'get_all_bots'):
            return await self.service_class.get_all_bots(db)
        elif hasattr(self.service_class, 'get_all_cats'):
            return await self.service_class.get_all_cats(db)
        else:
            raise NotImplementedError("Get all method not found")
    
    async def get_item_by_id(self, db: AsyncSession, item_id: str) -> Any:
        """Adapt get by ID operation."""
        if hasattr(self.service_class, 'get_bot_by_id'):
            return await self.service_class.get_bot_by_id(db, item_id)
        elif hasattr(self.service_class, 'get_cat_by_id'):
            return await self.service_class.get_cat_by_id(db, item_id)
        else:
            raise NotImplementedError("Get by ID method not found")
    
    async def update_item(self, item_id: str, item: Any, db: AsyncSession) -> Any:
        """Adapt update operation."""
        if hasattr(self.service_class, 'update_bot'):
            return await self.service_class.update_bot(item_id, item, db)
        elif hasattr(self.service_class, 'update_cat'):
            return await self.service_class.update_cat(item_id, item, db)
        else:
            raise NotImplementedError("Update method not found")
    
    async def delete_item(self, item_id: str, db: AsyncSession) -> Any:
        """Adapt delete operation."""
        if hasattr(self.service_class, 'delete_bot'):
            return await self.service_class.delete_bot(item_id, db)
        elif hasattr(self.service_class, 'delete_cat'):
            return await self.service_class.delete_cat(item_id, db)
        else:
            raise NotImplementedError("Delete method not found")