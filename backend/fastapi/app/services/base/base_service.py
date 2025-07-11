from abc import ABC, abstractmethod
from typing import TypeVar, Generic, List, Any, Type, Optional, Dict
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel

from app.utils.logging import logger


ModelType = TypeVar("ModelType")
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
ResponseSchemaType = TypeVar("ResponseSchemaType", bound=BaseModel)
AllResponseSchemaType = TypeVar("AllResponseSchemaType", bound=BaseModel)
UpdateRequestSchemaType = TypeVar("UpdateRequestSchemaType", bound=BaseModel)
UpdateResponseSchemaType = TypeVar("UpdateResponseSchemaType", bound=BaseModel)
DeleteResponseSchemaType = TypeVar("DeleteResponseSchemaType", bound=BaseModel)


class BaseService(
    ABC,
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
    """Base service class for common CRUD operations."""
    
    model: Type[ModelType]
    response_schema: Type[ResponseSchemaType]
    all_response_schema: Type[AllResponseSchemaType]
    update_response_schema: Type[UpdateResponseSchemaType]
    delete_response_schema: Type[DeleteResponseSchemaType]
    
    @classmethod
    async def create(
        cls, 
        db: AsyncSession, 
        item_data: CreateSchemaType
    ) -> ResponseSchemaType:
        """Create a new item."""
        try:
            new_item = cls.model(**item_data.model_dump())
            db.add(new_item)
            await db.commit()
            await db.refresh(new_item)
            
            logger.info(f"{cls.model.__name__}を作成しました: {new_item.id}")
            return cls.response_schema.model_validate(new_item)
        except Exception as e:
            await db.rollback()
            logger.error(f"{cls.model.__name__}の作成中にエラーが発生しました: {str(e)}")
            raise e
    
    @classmethod
    async def get_all(cls, db: AsyncSession) -> AllResponseSchemaType:
        """Get all items."""
        try:
            result = await db.execute(select(cls.model))
            items = result.scalars().all()
            
            item_responses = [cls.response_schema.model_validate(item) for item in items]
            logger.info(f"{len(item_responses)}件の{cls.model.__name__}を取得しました")
            
            # Construct the all response dynamically
            return cls.all_response_schema(**{cls._get_collection_field_name(): item_responses})
        except Exception as e:
            logger.error(f"{cls.model.__name__}の取得中にエラーが発生しました: {str(e)}")
            raise e
    
    @classmethod
    async def get_by_id(cls, db: AsyncSession, item_id: str) -> ResponseSchemaType:
        """Get item by ID."""
        try:
            result = await db.execute(select(cls.model).where(cls.model.id == item_id))
            item = result.scalar_one_or_none()
            
            if not item:
                raise ValueError(f"ID {item_id} の{cls.model.__name__}が見つかりません")
            
            return cls.response_schema.model_validate(item)
        except Exception as e:
            logger.error(f"{cls.model.__name__}の取得中にエラーが発生しました: {str(e)}")
            raise e
    
    @classmethod
    async def update(
        cls,
        item_id: str,
        update_data: UpdateRequestSchemaType,
        db: AsyncSession
    ) -> UpdateResponseSchemaType:
        """Update item by ID."""
        try:
            result = await db.execute(select(cls.model).where(cls.model.id == item_id))
            item = result.scalar_one_or_none()
            
            if not item:
                raise ValueError(f"ID {item_id} の{cls.model.__name__}が見つかりません")
            
            # Update fields that are provided
            update_dict = update_data.model_dump(exclude_unset=True)
            for field, value in update_dict.items():
                setattr(item, field, value)
            
            await db.commit()
            await db.refresh(item)
            
            logger.info(f"{cls.model.__name__}を更新しました: {item_id}")
            return cls.update_response_schema.model_validate(item)
        except Exception as e:
            await db.rollback()
            logger.error(f"{cls.model.__name__}の更新中にエラーが発生しました: {str(e)}")
            raise e
    
    @classmethod
    async def delete(cls, item_id: str, db: AsyncSession) -> DeleteResponseSchemaType:
        """Delete item by ID."""
        try:
            result = await db.execute(select(cls.model).where(cls.model.id == item_id))
            item = result.scalar_one_or_none()
            
            if not item:
                raise ValueError(f"ID {item_id} の{cls.model.__name__}が見つかりません")
            
            await db.delete(item)
            await db.commit()
            
            logger.info(f"{cls.model.__name__}を削除しました: {item_id}")
            return cls._create_delete_response(item_id)
        except Exception as e:
            await db.rollback()
            logger.error(f"{cls.model.__name__}の削除中にエラーが発生しました: {str(e)}")
            raise e
    
    @classmethod
    @abstractmethod
    def _get_collection_field_name(cls) -> str:
        """Get the field name for the collection in AllResponse schema."""
        pass
    
    @classmethod
    @abstractmethod
    def _create_delete_response(cls, item_id: str) -> DeleteResponseSchemaType:
        """Create a delete response instance."""
        pass


class LegacyServiceAdapter:
    """Adapter to make existing services compatible with the new base router."""
    
    def __init__(self, service_class: Type[Any]):
        self.service_class = service_class
    
    async def create(self, db: AsyncSession, item_data: Any) -> Any:
        """Adapter for create method."""
        if hasattr(self.service_class, 'create_chat_bot'):
            return await self.service_class.create_chat_bot(db, item_data)
        elif hasattr(self.service_class, 'create_cat'):
            return await self.service_class.create_cat(db, item_data)
        else:
            raise NotImplementedError(f"Create method not found for {self.service_class}")
    
    async def get_all(self, db: AsyncSession) -> Any:
        """Adapter for get_all method."""
        if hasattr(self.service_class, 'get_all_bots'):
            return await self.service_class.get_all_bots(db)
        elif hasattr(self.service_class, 'get_all_cats'):
            return await self.service_class.get_all_cats(db)
        else:
            raise NotImplementedError(f"Get all method not found for {self.service_class}")
    
    async def get_by_id(self, db: AsyncSession, item_id: str) -> Any:
        """Adapter for get_by_id method."""
        if hasattr(self.service_class, 'get_bot_by_id'):
            return await self.service_class.get_bot_by_id(db, item_id)
        elif hasattr(self.service_class, 'get_cat_by_id'):
            return await self.service_class.get_cat_by_id(db, item_id)
        else:
            raise NotImplementedError(f"Get by ID method not found for {self.service_class}")
    
    async def update(self, item_id: str, update_data: Any, db: AsyncSession) -> Any:
        """Adapter for update method."""
        if hasattr(self.service_class, 'update_bot'):
            return await self.service_class.update_bot(item_id, update_data, db)
        elif hasattr(self.service_class, 'update_cat'):
            return await self.service_class.update_cat(item_id, update_data, db)
        else:
            raise NotImplementedError(f"Update method not found for {self.service_class}")
    
    async def delete(self, item_id: str, db: AsyncSession) -> Any:
        """Adapter for delete method."""
        if hasattr(self.service_class, 'delete_bot'):
            return await self.service_class.delete_bot(item_id, db)
        elif hasattr(self.service_class, 'delete_cat'):
            return await self.service_class.delete_cat(item_id, db)
        else:
            raise NotImplementedError(f"Delete method not found for {self.service_class}")