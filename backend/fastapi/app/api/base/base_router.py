from typing import TypeVar, Generic, Type, Any, Dict, Optional
from abc import ABC, abstractmethod

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel

from app.db.database import get_db
from app.utils.logging import logger

# Type variables for generic classes
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
ResponseSchemaType = TypeVar("ResponseSchemaType", bound=BaseModel)
AllResponseSchemaType = TypeVar("AllResponseSchemaType", bound=BaseModel)
UpdateRequestSchemaType = TypeVar("UpdateRequestSchemaType", bound=BaseModel)
UpdateResponseSchemaType = TypeVar("UpdateResponseSchemaType", bound=BaseModel)
DeleteResponseSchemaType = TypeVar("DeleteResponseSchemaType", bound=BaseModel)


class BaseRouter(ABC):
    """Base router class for common functionality"""
    
    def __init__(self, prefix: str, tags: list[str]):
        self.router = APIRouter(prefix=prefix, tags=tags)
        self._setup_routes()
    
    @abstractmethod
    def _setup_routes(self):
        """Setup routes for the router"""
        pass
    
    @staticmethod
    def handle_error(error: Exception, operation: str, entity: str) -> HTTPException:
        """Centralized error handling"""
        if isinstance(error, ValueError):
            logger.error(f"{entity}{operation}エラー: {str(error)}")
            return HTTPException(status_code=404, detail=str(error))
        else:
            logger.error(f"{entity}{operation}エラー: {str(error)}")
            return HTTPException(status_code=500, detail=str(error))


class BaseCRUDRouter(
    BaseRouter, 
    Generic[
        CreateSchemaType,
        ResponseSchemaType,
        AllResponseSchemaType,
        UpdateRequestSchemaType,
        UpdateResponseSchemaType,
        DeleteResponseSchemaType
    ]
):
    """Base CRUD router with generic type support"""
    
    def __init__(
        self, 
        prefix: str, 
        tags: list[str],
        service_class: Type[Any],
        create_schema: Type[CreateSchemaType],
        response_schema: Type[ResponseSchemaType],
        all_response_schema: Type[AllResponseSchemaType],
        update_request_schema: Type[UpdateRequestSchemaType],
        update_response_schema: Type[UpdateResponseSchemaType],
        delete_response_schema: Type[DeleteResponseSchemaType],
        entity_name: str
    ):
        self.service_class = service_class
        self.create_schema = create_schema
        self.response_schema = response_schema
        self.all_response_schema = all_response_schema
        self.update_request_schema = update_request_schema
        self.update_response_schema = update_response_schema
        self.delete_response_schema = delete_response_schema
        self.entity_name = entity_name
        
        super().__init__(prefix, tags)
    
    def _setup_routes(self):
        """Setup standard CRUD routes"""
        
        @self.router.post("/", response_model=self.response_schema)
        async def create_entity(
            entity: self.create_schema, 
            db: AsyncSession = Depends(get_db)
        ):
            try:
                return await self.service_class.create_entity(db, entity)
            except Exception as e:
                raise self.handle_error(e, "作成", self.entity_name)
        
        @self.router.get("/", response_model=self.all_response_schema)
        async def get_all_entities(db: AsyncSession = Depends(get_db)):
            try:
                return await self.service_class.get_all_entities(db)
            except Exception as e:
                raise self.handle_error(e, "取得", self.entity_name)
        
        @self.router.get("/{entity_id}", response_model=self.response_schema)
        async def get_entity(
            entity_id: str, 
            db: AsyncSession = Depends(get_db)
        ):
            try:
                return await self.service_class.get_entity_by_id(db, entity_id)
            except Exception as e:
                raise self.handle_error(e, "取得", self.entity_name)
        
        @self.router.put("/{entity_id}", response_model=self.update_response_schema)
        async def update_entity(
            entity_id: str,
            request: self.update_request_schema,
            db: AsyncSession = Depends(get_db)
        ):
            try:
                return await self.service_class.update_entity(entity_id, request, db)
            except Exception as e:
                raise self.handle_error(e, "更新", self.entity_name)
        
        @self.router.delete("/{entity_id}", response_model=self.delete_response_schema)
        async def delete_entity(
            entity_id: str,
            db: AsyncSession = Depends(get_db)
        ):
            try:
                return await self.service_class.delete_entity(entity_id, db)
            except Exception as e:
                raise self.handle_error(e, "削除", self.entity_name)