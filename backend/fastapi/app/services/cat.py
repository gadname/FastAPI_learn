from app.models.cat import Cat
from app.schemas.cat import (
    CatCreate,
    CatResponse,
    CatAllResponse,
    UpdateCatRequest,
    UpdateCatResponse,
    DeleteCatResponse,
)
from app.services.base.base_service import BaseService


class CatService(BaseService[
    Cat,
    CatCreate,
    CatResponse,
    CatAllResponse,
    UpdateCatRequest,
    UpdateCatResponse,
    DeleteCatResponse
]):
    def __init__(self):
        super().__init__(
            model=Cat,
            response_schema=CatResponse,
            all_response_schema=CatAllResponse,
            update_response_schema=UpdateCatResponse,
            delete_response_schema=DeleteCatResponse,
            entity_name="猫",
            entity_name_plural="cats"
        )
    
    # The base service provides all CRUD operations
    # create_entity, get_all_entities, get_entity_by_id, update_entity, delete_entity
    
    # Add cat-specific methods if needed
    @classmethod
    async def create_cat(cls, db, cat_data):
        """Legacy method for backward compatibility"""
        return await cls.create_entity(db, cat_data)
    
    @classmethod
    async def get_all_cats(cls, db):
        """Legacy method for backward compatibility"""
        return await cls.get_all_entities(db)
    
    @classmethod
    async def get_cat_by_id(cls, db, cat_id):
        """Legacy method for backward compatibility"""
        return await cls.get_entity_by_id(db, cat_id)
    
    @classmethod
    async def update_cat(cls, cat_id, update_data, db):
        """Legacy method for backward compatibility"""
        return await cls.update_entity(cat_id, update_data, db)
    
    @classmethod
    async def delete_cat(cls, cat_id, db):
        """Legacy method for backward compatibility"""
        return await cls.delete_entity(cat_id, db)