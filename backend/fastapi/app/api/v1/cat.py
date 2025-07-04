from fastapi import APIRouter, Depends
from fastapi import HTTPException

from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.cat import (
    CatCreate,
    CatResponse,
    CatAllResponse,
    UpdateCatResponse,
    UpdateCatRequest,
    DeleteCatResponse,
)

from app.db.database import get_db
from app.services.cat import CatService
from app.utils.logging import logger # Ensure logger is imported
from app.api.v1.base_router import generic_router_factory
from typing import List # Required for List type hint if not already present

# Adapter class to bridge CatService and generic_router_factory
class CatServiceAdapter:
    # Using CatService directly as it contains static methods
    # No need to instantiate CatService itself if all methods are static.
    # db_service = CatService (this line is not needed if directly calling static methods)

    async def create(self, db: AsyncSession, obj_in: CatCreate) -> CatResponse:
        return await CatService.create_cat(db=db, cat_data=obj_in)

    async def get_multi(self, db: AsyncSession, skip: int = 0, limit: int = 100) -> CatAllResponse:
        # CatService.get_all_cats doesn't support pagination (skip, limit).
        # It directly returns CatAllResponse as required.
        return await CatService.get_all_cats(db=db)

    async def get(self, db: AsyncSession, id: str) -> CatResponse:
        return await CatService.get_cat_by_id(db=db, cat_id=id)

    async def update(self, db: AsyncSession, db_obj: CatResponse, obj_in: UpdateCatRequest) -> UpdateCatResponse:
        # generic_router_factory first fetches the object (db_obj), then passes it to update.
        # CatService.update_cat needs cat_id and the request schema.
        if not hasattr(db_obj, 'id'):
            raise ValueError("db_obj must have an id attribute for update")
        return await CatService.update_cat(cat_id=db_obj.id, update_data=obj_in, db=db)

    async def remove(self, db: AsyncSession, id: str) -> DeleteCatResponse:
        return await CatService.delete_cat(cat_id=id, db=db)

# Instantiate the adapter
adapted_cat_service = CatServiceAdapter()

# Create the router using the generic factory and the adapter
router = generic_router_factory(
    service=adapted_cat_service,
    tags=["cat"],
    prefix="/cat",
    response_model=CatResponse,
    create_schema=CatCreate,
    update_schema=UpdateCatRequest,
    get_all_response_model=CatAllResponse, # Using CatAllResponse directly
    update_response_model=UpdateCatResponse,
    delete_response_model=DeleteCatResponse,
)