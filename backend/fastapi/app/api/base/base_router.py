from abc import ABC, abstractmethod
from typing import TypeVar, Generic, List, Any, Type, Optional, Union
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel

from app.db.database import get_db
from app.utils.logging import logger
from app.services.base.base_service import LegacyServiceAdapter


ModelType = TypeVar("ModelType", bound=BaseModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
ResponseSchemaType = TypeVar("ResponseSchemaType", bound=BaseModel)
AllResponseSchemaType = TypeVar("AllResponseSchemaType", bound=BaseModel)
UpdateRequestSchemaType = TypeVar("UpdateRequestSchemaType", bound=BaseModel)
UpdateResponseSchemaType = TypeVar("UpdateResponseSchemaType", bound=BaseModel)
DeleteResponseSchemaType = TypeVar("DeleteResponseSchemaType", bound=BaseModel)


class BaseRouter(ABC):
    """Base router class for common router functionality."""
    
    def __init__(self, prefix: str, tags: List[str]):
        self.router = APIRouter(prefix=prefix, tags=tags)
    
    def get_router(self) -> APIRouter:
        """Get the FastAPI router instance."""
        return self.router


class BaseCRUDRouter(
    BaseRouter,
    Generic[
        ModelType,
        CreateSchemaType,
        ResponseSchemaType,
        AllResponseSchemaType,
        UpdateRequestSchemaType,
        UpdateResponseSchemaType,
        DeleteResponseSchemaType,
    ],
):
    """Base CRUD router class with standardized CRUD operations."""
    
    def __init__(
        self,
        prefix: str,
        tags: List[str],
        service_class: Type[Any],
        response_model: Type[ResponseSchemaType],
        all_response_model: Type[AllResponseSchemaType],
        update_response_model: Type[UpdateResponseSchemaType],
        delete_response_model: Type[DeleteResponseSchemaType],
        resource_name: str,
        resource_name_ja: str,
        use_legacy_adapter: bool = False,
    ):
        super().__init__(prefix, tags)
        self.service_class = service_class
        self.response_model = response_model
        self.all_response_model = all_response_model
        self.update_response_model = update_response_model
        self.delete_response_model = delete_response_model
        self.resource_name = resource_name
        self.resource_name_ja = resource_name_ja
        
        # Use adapter for legacy services
        if use_legacy_adapter:
            self.service = LegacyServiceAdapter(service_class)
        else:
            self.service = service_class
        
        self._register_routes()
    
    def _register_routes(self):
        """Register all CRUD routes."""
        self.router.post("/", response_model=self.response_model)(self._create)
        self.router.get("/", response_model=self.all_response_model)(self._get_all)
        self.router.get("/{item_id}", response_model=self.response_model)(self._get_by_id)
        self.router.put("/{item_id}", response_model=self.update_response_model)(self._update)
        self.router.delete("/{item_id}", response_model=self.delete_response_model)(self._delete)
    
    async def _create(
        self,
        item: CreateSchemaType,
        db: AsyncSession = Depends(get_db)
    ) -> ResponseSchemaType:
        """Create a new item."""
        try:
            return await self.service.create(db, item)
        except Exception as e:
            logger.error(f"{self.resource_name_ja}作成エラー: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))
    
    async def _get_all(
        self,
        db: AsyncSession = Depends(get_db)
    ) -> AllResponseSchemaType:
        """Get all items."""
        try:
            return await self.service.get_all(db)
        except Exception as e:
            logger.error(f"{self.resource_name_ja}取得エラー: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))
    
    async def _get_by_id(
        self,
        item_id: str,
        db: AsyncSession = Depends(get_db)
    ) -> ResponseSchemaType:
        """Get item by ID."""
        try:
            return await self.service.get_by_id(db, item_id)
        except ValueError as e:
            logger.error(f"{self.resource_name_ja}が見つかりません: {str(e)}")
            raise HTTPException(status_code=404, detail=str(e))
        except Exception as e:
            logger.error(f"{self.resource_name_ja}取得エラー: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))
    
    async def _update(
        self,
        item_id: str,
        request: UpdateRequestSchemaType,
        db: AsyncSession = Depends(get_db)
    ) -> UpdateResponseSchemaType:
        """Update item by ID."""
        try:
            return await self.service.update(item_id, request, db)
        except ValueError as e:
            logger.error(f"{self.resource_name_ja}が見つかりません: {str(e)}")
            raise HTTPException(status_code=404, detail=str(e))
        except Exception as e:
            logger.error(f"{self.resource_name_ja}更新エラー: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))
    
    async def _delete(
        self,
        item_id: str,
        db: AsyncSession = Depends(get_db)
    ) -> DeleteResponseSchemaType:
        """Delete item by ID."""
        try:
            return await self.service.delete(item_id, db)
        except ValueError as e:
            logger.error(f"{self.resource_name_ja}が見つかりません: {str(e)}")
            raise HTTPException(status_code=404, detail=str(e))
        except Exception as e:
            logger.error(f"{self.resource_name_ja}削除エラー: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))