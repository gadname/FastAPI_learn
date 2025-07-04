from fastapi import APIRouter, Depends
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
from app.utils.router_utils import (
    handle_create_operation,
    handle_get_operation,
    handle_update_operation,
    handle_delete_operation,
)


router = APIRouter(prefix="/cat", tags=["cat"])


@router.post("/", response_model=CatResponse)
@handle_create_operation("猫")
async def create_cat(cat: CatCreate, db: AsyncSession = Depends(get_db)) -> CatResponse:
    return await CatService.create_cat(db, cat)


@router.get("/", response_model=CatAllResponse)
@handle_get_operation("猫")
async def get_all_cats(db: AsyncSession = Depends(get_db)) -> CatAllResponse:
    return await CatService.get_all_cats(db)


@router.get("/{cat_id}", response_model=CatResponse)
@handle_get_operation("猫")
async def get_cat(cat_id: str, db: AsyncSession = Depends(get_db)) -> CatResponse:
    return await CatService.get_cat_by_id(db, cat_id)


@router.put("/{cat_id}", response_model=UpdateCatResponse)
@handle_update_operation("猫")
async def update_cat(
    cat_id: str, request: UpdateCatRequest, db: AsyncSession = Depends(get_db)
) -> UpdateCatResponse:
    return await CatService.update_cat(cat_id, request, db)


@router.delete("/{cat_id}", response_model=DeleteCatResponse)
@handle_delete_operation("猫")
async def delete_cat(
    cat_id: str, db: AsyncSession = Depends(get_db)
) -> DeleteCatResponse:
    return await CatService.delete_cat(cat_id, db)
