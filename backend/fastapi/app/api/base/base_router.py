"""Base router classes for standardized API routing."""

from typing import Any, Dict, Generic, List, Type, TypeVar, Union

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.services.base.base_service import BaseService, LegacyServiceAdapter
from app.utils.logging import logger

# Type variables for generic router operations
CreateSchemaType = TypeVar("CreateSchemaType")
ResponseSchemaType = TypeVar("ResponseSchemaType")
UpdateSchemaType = TypeVar("UpdateSchemaType")
AllResponseSchemaType = TypeVar("AllResponseSchemaType")


class BaseRouter:
    """
    Base router class providing common functionality for all routers.
    
    This class provides centralized error handling and common utilities
    that can be used by all router implementations.
    """
    
    def __init__(self, prefix: str, tags: List[str]):
        self.prefix = prefix
        self.tags = tags
        self.router = APIRouter(prefix=prefix, tags=tags)
    
    def _handle_error(self, error: Exception, operation: str) -> None:
        """
        Centralized error handling for all router operations.
        
        Args:
            error: The exception that occurred
            operation: Description of the operation that failed
        
        Raises:
            HTTPException: With appropriate status code and message
        """
        error_msg = str(error)
        
        if isinstance(error, ValueError):
            logger.error(f"{operation}でエラーが発生しました: {error_msg}")
            raise HTTPException(status_code=404, detail=error_msg)
        else:
            logger.error(f"{operation}でエラーが発生しました: {error_msg}")
            raise HTTPException(status_code=500, detail=error_msg)


class BaseCRUDRouter(BaseRouter, Generic[CreateSchemaType, ResponseSchemaType, UpdateSchemaType, AllResponseSchemaType]):
    """
    Base CRUD router providing standardized CRUD operations.
    
    This class eliminates code duplication by providing common CRUD endpoints
    that can be used by all resource routers.
    """
    
    def __init__(
        self,
        prefix: str,
        tags: List[str],
        service: Union[Type[BaseService], Any],
        create_schema: Type[CreateSchemaType],
        response_schema: Type[ResponseSchemaType],
        update_schema: Type[UpdateSchemaType],
        all_response_schema: Type[AllResponseSchemaType] = None,
        delete_response_schema: Type[Any] = None,
        resource_name: str = "item"
    ):
        super().__init__(prefix, tags)
        
        # Use adapter for legacy services
        if hasattr(service, 'create_chat_bot') or hasattr(service, 'create_cat'):
            self.service = LegacyServiceAdapter(service)
        else:
            self.service = service
            
        self.create_schema = create_schema
        self.response_schema = response_schema
        self.update_schema = update_schema
        self.all_response_schema = all_response_schema or List[response_schema]
        self.delete_response_schema = delete_response_schema
        self.resource_name = resource_name
        
        # Register CRUD endpoints
        self._register_endpoints()
    
    def _register_endpoints(self) -> None:
        """Register all CRUD endpoints."""
        # Create endpoint
        self.router.post("/", response_model=self.response_schema)(self._create_item)
        
        # Get all endpoint
        self.router.get("/", response_model=self.all_response_schema)(self._get_all_items)
        
        # Get by ID endpoint
        self.router.get("/{item_id}", response_model=self.response_schema)(self._get_item_by_id)
        
        # Update endpoint
        self.router.put("/{item_id}", response_model=self.response_schema)(self._update_item)
        
        # Delete endpoint
        if self.delete_response_schema:
            self.router.delete("/{item_id}", response_model=self.delete_response_schema)(self._delete_item)
        else:
            self.router.delete("/{item_id}")(self._delete_item)
    
    async def _create_item(
        self, 
        item: CreateSchemaType, 
        db: AsyncSession = Depends(get_db)
    ) -> ResponseSchemaType:
        """Create a new item."""
        try:
            return await self.service.create_item(db, item)
        except Exception as e:
            self._handle_error(e, f"{self.resource_name}作成")
    
    async def _get_all_items(
        self, 
        db: AsyncSession = Depends(get_db)
    ) -> AllResponseSchemaType:
        """Get all items."""
        try:
            return await self.service.get_all_items(db)
        except Exception as e:
            self._handle_error(e, f"{self.resource_name}取得")
    
    async def _get_item_by_id(
        self, 
        item_id: str, 
        db: AsyncSession = Depends(get_db)
    ) -> ResponseSchemaType:
        """Get item by ID."""
        try:
            return await self.service.get_item_by_id(db, item_id)
        except Exception as e:
            self._handle_error(e, f"{self.resource_name}取得")
    
    async def _update_item(
        self, 
        item_id: str, 
        item: UpdateSchemaType, 
        db: AsyncSession = Depends(get_db)
    ) -> ResponseSchemaType:
        """Update an item."""
        try:
            return await self.service.update_item(item_id, item, db)
        except Exception as e:
            self._handle_error(e, f"{self.resource_name}更新")
    
    async def _delete_item(
        self, 
        item_id: str, 
        db: AsyncSession = Depends(get_db)
    ) -> Any:
        """Delete an item."""
        try:
            return await self.service.delete_item(item_id, db)
        except Exception as e:
            self._handle_error(e, f"{self.resource_name}削除")