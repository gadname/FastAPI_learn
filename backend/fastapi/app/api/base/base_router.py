from typing import TypeVar, Generic, Type, Any, Dict, Optional
from abc import ABC, abstractmethod
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from app.db.database import get_db
from app.utils.logging import logger

# Type variables for generic support
TCreateSchema = TypeVar("TCreateSchema", bound=BaseModel)
TResponseSchema = TypeVar("TResponseSchema", bound=BaseModel)
TAllResponseSchema = TypeVar("TAllResponseSchema", bound=BaseModel)
TUpdateRequestSchema = TypeVar("TUpdateRequestSchema", bound=BaseModel)
TUpdateResponseSchema = TypeVar("TUpdateResponseSchema", bound=BaseModel)
TDeleteResponseSchema = TypeVar("TDeleteResponseSchema", bound=BaseModel)
TService = TypeVar("TService")


class BaseRouter(ABC):
    """Base router class for common router functionality"""
    
    def __init__(self, prefix: str, tags: list[str]):
        self.router = APIRouter(prefix=prefix, tags=tags)
    
    @abstractmethod
    def setup_routes(self) -> None:
        """Setup routes for this router"""
        pass


class BaseCRUDRouter(
    BaseRouter,
    Generic[
        TCreateSchema,
        TResponseSchema,
        TAllResponseSchema,
        TUpdateRequestSchema,
        TUpdateResponseSchema,
        TDeleteResponseSchema,
        TService
    ]
):
    """Base CRUD router with generic type support"""
    
    def __init__(
        self,
        prefix: str,
        tags: list[str],
        service_class: Type[TService],
        create_schema: Type[TCreateSchema],
        response_schema: Type[TResponseSchema],
        all_response_schema: Type[TAllResponseSchema],
        update_request_schema: Type[TUpdateRequestSchema],
        update_response_schema: Type[TUpdateResponseSchema],
        delete_response_schema: Type[TDeleteResponseSchema],
        entity_name: str,
        entity_name_jp: str,
        service_method_names: Optional[Dict[str, str]] = None,
    ):
        super().__init__(prefix, tags)
        self.service_class = service_class
        self.create_schema = create_schema
        self.response_schema = response_schema
        self.all_response_schema = all_response_schema
        self.update_request_schema = update_request_schema
        self.update_response_schema = update_response_schema
        self.delete_response_schema = delete_response_schema
        self.entity_name = entity_name
        self.entity_name_jp = entity_name_jp
        
        # Set default method names or use provided ones
        default_method_names = {
            "create": f"create_{entity_name}",
            "get_all": f"get_all_{entity_name}s",
            "get_by_id": f"get_{entity_name}_by_id",
            "update": f"update_{entity_name}",
            "delete": f"delete_{entity_name}",
        }
        self.service_method_names = service_method_names or default_method_names
        
        self.setup_routes()
    
    def setup_routes(self) -> None:
        """Setup CRUD routes"""
        
        @self.router.post("/", response_model=self.response_schema)
        async def create_entity(
            entity: self.create_schema,
            db: AsyncSession = Depends(get_db)
        ) -> self.response_schema:
            try:
                method_name = self.service_method_names["create"]
                if hasattr(self.service_class, method_name):
                    return await getattr(self.service_class, method_name)(db, entity)
                else:
                    raise NotImplementedError(f"Method {method_name} not found in service")
            except Exception as e:
                logger.error(f"{self.entity_name_jp}作成エラー: {str(e)}")
                raise HTTPException(status_code=500, detail=str(e))
        
        @self.router.get("/", response_model=self.all_response_schema)
        async def get_all_entities(
            db: AsyncSession = Depends(get_db)
        ) -> self.all_response_schema:
            try:
                method_name = self.service_method_names["get_all"]
                if hasattr(self.service_class, method_name):
                    return await getattr(self.service_class, method_name)(db)
                else:
                    raise NotImplementedError(f"Method {method_name} not found in service")
            except Exception as e:
                logger.error(f"{self.entity_name_jp}取得エラー: {str(e)}")
                raise HTTPException(status_code=500, detail=str(e))
        
        @self.router.get("/{entity_id}", response_model=self.response_schema)
        async def get_entity(
            entity_id: str,
            db: AsyncSession = Depends(get_db)
        ) -> self.response_schema:
            try:
                method_name = self.service_method_names["get_by_id"]
                if hasattr(self.service_class, method_name):
                    return await getattr(self.service_class, method_name)(db, entity_id)
                else:
                    raise NotImplementedError(f"Method {method_name} not found in service")
            except ValueError as e:
                logger.error(f"{self.entity_name_jp}が見つかりません: {str(e)}")
                raise HTTPException(status_code=404, detail=str(e))
            except Exception as e:
                logger.error(f"{self.entity_name_jp}取得エラー: {str(e)}")
                raise HTTPException(status_code=500, detail=str(e))
        
        @self.router.put("/{entity_id}", response_model=self.update_response_schema)
        async def update_entity(
            entity_id: str,
            request: self.update_request_schema,
            db: AsyncSession = Depends(get_db)
        ) -> self.update_response_schema:
            try:
                method_name = self.service_method_names["update"]
                if hasattr(self.service_class, method_name):
                    return await getattr(self.service_class, method_name)(entity_id, request, db)
                else:
                    raise NotImplementedError(f"Method {method_name} not found in service")
            except ValueError as e:
                logger.error(f"{self.entity_name_jp}が見つかりません: {str(e)}")
                raise HTTPException(status_code=404, detail=str(e))
            except Exception as e:
                logger.error(f"{self.entity_name_jp}更新エラー: {str(e)}")
                raise HTTPException(status_code=500, detail=str(e))
        
        @self.router.delete("/{entity_id}", response_model=self.delete_response_schema)
        async def delete_entity(
            entity_id: str,
            db: AsyncSession = Depends(get_db)
        ) -> self.delete_response_schema:
            try:
                method_name = self.service_method_names["delete"]
                if hasattr(self.service_class, method_name):
                    return await getattr(self.service_class, method_name)(entity_id, db)
                else:
                    raise NotImplementedError(f"Method {method_name} not found in service")
            except ValueError as e:
                logger.error(f"{self.entity_name_jp}が見つかりません: {str(e)}")
                raise HTTPException(status_code=404, detail=str(e))
            except Exception as e:
                logger.error(f"{self.entity_name_jp}削除エラー: {str(e)}")
                raise HTTPException(status_code=500, detail=str(e))