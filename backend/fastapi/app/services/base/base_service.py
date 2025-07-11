from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Type, Any, Dict, Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel
from app.utils.logging import logger

# Type variables for generic support
TModel = TypeVar("TModel")
TCreateSchema = TypeVar("TCreateSchema", bound=BaseModel)
TResponseSchema = TypeVar("TResponseSchema", bound=BaseModel)
TAllResponseSchema = TypeVar("TAllResponseSchema", bound=BaseModel)
TUpdateRequestSchema = TypeVar("TUpdateRequestSchema", bound=BaseModel)
TUpdateResponseSchema = TypeVar("TUpdateResponseSchema", bound=BaseModel)
TDeleteResponseSchema = TypeVar("TDeleteResponseSchema", bound=BaseModel)


class BaseService(ABC):
    """Abstract base service class for common database operations"""
    
    @abstractmethod
    def get_model(self) -> Type[TModel]:
        """Return the SQLAlchemy model class"""
        pass
    
    @abstractmethod
    def get_entity_name(self) -> str:
        """Return the entity name (e.g., 'cat', 'bot')"""
        pass
    
    @abstractmethod
    def get_entity_name_jp(self) -> str:
        """Return the Japanese entity name (e.g., '猫', 'ボット')"""
        pass


class LegacyServiceAdapter:
    """Adapter to make existing services work with the new base router system"""
    
    def __init__(self, service_class: Type[Any]):
        self.service_class = service_class
    
    def __getattr__(self, name: str):
        """Delegate attribute access to the wrapped service class"""
        return getattr(self.service_class, name)


# Generic CRUD operations that can be used by concrete service classes
class BaseCRUDService(
    BaseService,
    Generic[
        TModel,
        TCreateSchema,
        TResponseSchema,
        TAllResponseSchema,
        TUpdateRequestSchema,
        TUpdateResponseSchema,
        TDeleteResponseSchema
    ]
):
    """Base CRUD service with generic type support"""
    
    def __init__(
        self,
        model: Type[TModel],
        response_schema: Type[TResponseSchema],
        all_response_schema: Type[TAllResponseSchema],
        update_response_schema: Type[TUpdateResponseSchema],
        delete_response_schema: Type[TDeleteResponseSchema],
        entity_name: str,
        entity_name_jp: str,
    ):
        self.model = model
        self.response_schema = response_schema
        self.all_response_schema = all_response_schema
        self.update_response_schema = update_response_schema
        self.delete_response_schema = delete_response_schema
        self.entity_name = entity_name
        self.entity_name_jp = entity_name_jp
    
    def get_model(self) -> Type[TModel]:
        return self.model
    
    def get_entity_name(self) -> str:
        return self.entity_name
    
    def get_entity_name_jp(self) -> str:
        return self.entity_name_jp
    
    async def create_entity(
        self,
        db: AsyncSession,
        entity_data: TCreateSchema
    ) -> TResponseSchema:
        """Create a new entity"""
        try:
            new_entity = self.model(**entity_data.model_dump())
            db.add(new_entity)
            await db.commit()
            await db.refresh(new_entity)
            
            logger.info(f"{self.entity_name_jp}を作成しました: {new_entity.id}")
            return self.response_schema.model_validate(new_entity)
        except Exception as e:
            await db.rollback()
            logger.error(f"{self.entity_name_jp}の作成中にエラーが発生しました: {str(e)}")
            raise e
    
    async def get_all_entities(self, db: AsyncSession) -> TAllResponseSchema:
        """Get all entities"""
        try:
            result = await db.execute(select(self.model))
            entities = result.scalars().all()
            
            entity_responses = [self.response_schema.model_validate(entity) for entity in entities]
            logger.info(f"{len(entity_responses)}件の{self.entity_name_jp}を取得しました")
            
            # Dynamically create the response based on the schema
            if hasattr(self.all_response_schema, 'model_fields'):
                # Find the field that should contain the list of entities
                list_field = None
                for field_name, field_info in self.all_response_schema.model_fields.items():
                    if hasattr(field_info, 'annotation') and 'List' in str(field_info.annotation):
                        list_field = field_name
                        break
                
                if list_field:
                    return self.all_response_schema(**{list_field: entity_responses})
                else:
                    # Fallback: assume first field is the list field
                    first_field = list(self.all_response_schema.model_fields.keys())[0]
                    return self.all_response_schema(**{first_field: entity_responses})
            
            return self.all_response_schema(entities=entity_responses)
        except Exception as e:
            logger.error(f"{self.entity_name_jp}の取得中にエラーが発生しました: {str(e)}")
            raise e
    
    async def get_entity_by_id(self, db: AsyncSession, entity_id: str) -> TResponseSchema:
        """Get entity by ID"""
        try:
            result = await db.execute(select(self.model).where(self.model.id == entity_id))
            entity = result.scalar_one_or_none()
            
            if not entity:
                raise ValueError(f"ID {entity_id} の{self.entity_name_jp}が見つかりません")
            
            return self.response_schema.model_validate(entity)
        except Exception as e:
            logger.error(f"{self.entity_name_jp}の取得中にエラーが発生しました: {str(e)}")
            raise e
    
    async def update_entity(
        self,
        entity_id: str,
        update_data: TUpdateRequestSchema,
        db: AsyncSession
    ) -> TUpdateResponseSchema:
        """Update entity"""
        try:
            result = await db.execute(select(self.model).where(self.model.id == entity_id))
            entity = result.scalar_one_or_none()
            
            if not entity:
                raise ValueError(f"ID {entity_id} の{self.entity_name_jp}が見つかりません")
            
            # Update fields
            update_dict = update_data.model_dump(exclude_unset=True)
            for field, value in update_dict.items():
                if hasattr(entity, field):
                    setattr(entity, field, value)
            
            await db.commit()
            await db.refresh(entity)
            
            logger.info(f"{self.entity_name_jp}を更新しました: {entity_id}")
            return self.update_response_schema.model_validate(entity)
        except Exception as e:
            await db.rollback()
            logger.error(f"{self.entity_name_jp}の更新中にエラーが発生しました: {str(e)}")
            raise e
    
    async def delete_entity(
        self,
        entity_id: str,
        db: AsyncSession
    ) -> TDeleteResponseSchema:
        """Delete entity"""
        try:
            result = await db.execute(select(self.model).where(self.model.id == entity_id))
            entity = result.scalar_one_or_none()
            
            if not entity:
                raise ValueError(f"ID {entity_id} の{self.entity_name_jp}が見つかりません")
            
            await db.delete(entity)
            await db.commit()
            
            logger.info(f"{self.entity_name_jp}を削除しました: {entity_id}")
            
            # Create response with appropriate fields
            response_data = {"id": entity_id}
            if hasattr(self.delete_response_schema, 'model_fields'):
                if 'message' in self.delete_response_schema.model_fields:
                    response_data["message"] = f"{self.entity_name_jp}を正常に削除しました"
            
            return self.delete_response_schema(**response_data)
        except Exception as e:
            await db.rollback()
            logger.error(f"{self.entity_name_jp}の削除中にエラーが発生しました: {str(e)}")
            raise e