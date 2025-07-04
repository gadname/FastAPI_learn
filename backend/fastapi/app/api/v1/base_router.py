from typing import Any, Callable, List, Type, TypeVar

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.utils.logger import logger

ModelType = TypeVar("ModelType")
CreateSchemaType = TypeVar("CreateSchemaType")
UpdateSchemaType = TypeVar("UpdateSchemaType")
GetAllModelT = TypeVar("GetAllModelT") # New TypeVar for get_all_response_model
ServiceType = TypeVar("ServiceType")


def generic_router_factory(
    service: ServiceType,
    tags: List[str],
    prefix: str,
    response_model: Type[ModelType],
    create_schema: Type[CreateSchemaType],
    update_schema: Type[UpdateSchemaType],
    get_all_response_model: Type[GetAllModelT], # Changed type hint
    update_response_model: Type[ModelType] = None,
    delete_response_model: Type[ModelType] = None,
) -> APIRouter:
    router = APIRouter(prefix=prefix, tags=tags)

    # Determine the response model for update and delete operations
    actual_update_response_model = update_response_model if update_response_model else response_model
    actual_delete_response_model = delete_response_model if delete_response_model else response_model

    @router.post("/", response_model=response_model, status_code=201)
    async def create_item(
        item_in: create_schema,
        db: AsyncSession = Depends(get_db),
    ) -> ModelType:
        try:
            item = await service.create(db, obj_in=item_in)
            return item
        except Exception as e:
            logger.error(f"Error creating item: {e}")
            raise HTTPException(status_code=500, detail="Internal server error")

    @router.get("/", response_model=get_all_response_model)
    async def get_all_items(
        db: AsyncSession = Depends(get_db),
        skip: int = 0,
        limit: int = 100,
    ) -> GetAllModelT: # Changed return type hint
        try:
            items = await service.get_multi(db, skip=skip, limit=limit)
            return items
        except Exception as e:
            logger.error(f"Error retrieving items: {e}")
            raise HTTPException(status_code=500, detail="Internal server error")

    @router.get("/{item_id}", response_model=response_model)
    async def get_item(
        item_id: Any,
        db: AsyncSession = Depends(get_db),
    ) -> ModelType:
        try:
            item = await service.get(db, id=item_id)
            if not item:
                raise ValueError("Item not found")
            return item
        except ValueError as e:
            logger.warning(f"Item not found: {item_id}, error: {e}")
            raise HTTPException(status_code=404, detail=str(e))
        except Exception as e:
            logger.error(f"Error retrieving item {item_id}: {e}")
            raise HTTPException(status_code=500, detail="Internal server error")

    @router.put("/{item_id}", response_model=actual_update_response_model)  # Use actual_update_response_model
    async def update_item(
        item_id: Any,
        item_in: update_schema,
        db: AsyncSession = Depends(get_db),
    ) -> ModelType:  # The return type hint might need adjustment if models differ significantly
        try:
            item = await service.get(db, id=item_id)
            if not item:
                raise ValueError("Item not found for update")
            updated_item = await service.update(db, db_obj=item, obj_in=item_in)
            return updated_item
        except ValueError as e:
            logger.warning(f"Item not found for update: {item_id}, error: {e}")
            raise HTTPException(status_code=404, detail=str(e))
        except Exception as e:
            logger.error(f"Error updating item {item_id}: {e}")
            raise HTTPException(status_code=500, detail="Internal server error")

    @router.delete("/{item_id}", response_model=actual_delete_response_model)  # Use actual_delete_response_model
    async def delete_item(
        item_id: Any,
        db: AsyncSession = Depends(get_db),
    ) -> ModelType:  # The return type hint might need to be Union[ModelType, DeleteModelType] if they differ
        try:
            item = await service.get(db, id=item_id)
            if not item:
                raise ValueError("Item not found for deletion")
            deleted_item = await service.remove(db, id=item_id)
            return deleted_item
        except ValueError as e:
            logger.warning(f"Item not found for deletion: {item_id}, error: {e}")
            raise HTTPException(status_code=404, detail=str(e))
        except Exception as e:
            logger.error(f"Error deleting item {item_id}: {e}")
            raise HTTPException(status_code=500, detail="Internal server error")

    return router
