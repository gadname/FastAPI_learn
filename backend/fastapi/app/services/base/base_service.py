from typing import TypeVar, Generic, Type, Any, List, Optional
from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel

from app.utils.logging import logger

# Type variables for generic classes  
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
        DeleteResponseSchemaType
    ]
):
    """Base service class for common database operations"""
    
    def __init__(
        self,
        model: Type[ModelType],
        response_schema: Type[ResponseSchemaType],
        all_response_schema: Type[AllResponseSchemaType],
        update_response_schema: Type[UpdateResponseSchemaType],
        delete_response_schema: Type[DeleteResponseSchemaType],
        entity_name: str,
        entity_name_plural: str
    ):
        self.model = model
        self.response_schema = response_schema
        self.all_response_schema = all_response_schema
        self.update_response_schema = update_response_schema
        self.delete_response_schema = delete_response_schema
        self.entity_name = entity_name
        self.entity_name_plural = entity_name_plural
    
    @classmethod
    async def create_entity(
        cls, 
        db: AsyncSession, 
        entity_data: CreateSchemaType
    ) -> ResponseSchemaType:
        """Create a new entity"""
        try:
            instance = cls()
            new_entity = instance.model(**entity_data.model_dump())
            db.add(new_entity)
            await db.commit()
            await db.refresh(new_entity)
            
            logger.info(f"{instance.entity_name}を作成しました: {new_entity.id}")
            return instance.response_schema.model_validate(new_entity)
        except Exception as e:
            await db.rollback()
            logger.error(f"{instance.entity_name}の作成中にエラーが発生しました: {str(e)}")
            raise e
    
    @classmethod
    async def get_all_entities(cls, db: AsyncSession) -> AllResponseSchemaType:
        """Get all entities"""
        try:
            instance = cls()
            result = await db.execute(select(instance.model))
            entities = result.scalars().all()
            
            entity_responses = [
                instance.response_schema.model_validate(entity) for entity in entities
            ]
            logger.info(f"{len(entity_responses)}件の{instance.entity_name}を取得しました")
            
            return instance.all_response_schema(**{instance.entity_name_plural: entity_responses})
        except Exception as e:
            instance = cls()
            logger.error(f"{instance.entity_name}の取得中にエラーが発生しました: {str(e)}")
            raise e
    
    @classmethod
    async def get_entity_by_id(
        cls, 
        db: AsyncSession, 
        entity_id: str
    ) -> ResponseSchemaType:
        """Get entity by ID"""
        try:
            instance = cls()
            result = await db.execute(
                select(instance.model).where(instance.model.id == entity_id)
            )
            entity = result.scalar_one_or_none()
            
            if not entity:
                raise ValueError(f"ID {entity_id} の{instance.entity_name}が見つかりません")
            
            return instance.response_schema.model_validate(entity)
        except Exception as e:
            instance = cls()
            logger.error(f"{instance.entity_name}の取得中にエラーが発生しました: {str(e)}")
            raise e
    
    @classmethod
    async def update_entity(
        cls,
        entity_id: str,
        update_data: UpdateRequestSchemaType,
        db: AsyncSession
    ) -> UpdateResponseSchemaType:
        """Update entity"""
        try:
            instance = cls()
            result = await db.execute(
                select(instance.model).where(instance.model.id == entity_id)
            )
            entity = result.scalar_one_or_none()
            
            if not entity:
                raise ValueError(f"ID {entity_id} の{instance.entity_name}が見つかりません")
            
            # Apply updates
            update_dict = update_data.model_dump(exclude_unset=True)
            for field, value in update_dict.items():
                setattr(entity, field, value)
            
            await db.commit()
            await db.refresh(entity)
            
            logger.info(f"{instance.entity_name}を更新しました: {entity_id}")
            return instance.update_response_schema.model_validate(entity)
        except Exception as e:
            await db.rollback()
            instance = cls()
            logger.error(f"{instance.entity_name}の更新中にエラーが発生しました: {str(e)}")
            raise e
    
    @classmethod
    async def delete_entity(
        cls,
        entity_id: str,
        db: AsyncSession
    ) -> DeleteResponseSchemaType:
        """Delete entity"""
        try:
            instance = cls()
            result = await db.execute(
                select(instance.model).where(instance.model.id == entity_id)
            )
            entity = result.scalar_one_or_none()
            
            if not entity:
                raise ValueError(f"ID {entity_id} の{instance.entity_name}が見つかりません")
            
            await db.delete(entity)
            await db.commit()
            
            logger.info(f"{instance.entity_name}を削除しました: {entity_id}")
            return instance.delete_response_schema(
                message=f"{instance.entity_name}を正常に削除しました",
                id=entity_id
            )
        except Exception as e:
            await db.rollback()
            instance = cls()
            logger.error(f"{instance.entity_name}の削除中にエラーが発生しました: {str(e)}")
            raise e