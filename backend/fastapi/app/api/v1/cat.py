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
from app.utils.logging import logger


router = APIRouter(prefix="/cat", tags=["cat"])


@router.post("/", response_model=CatResponse)
async def create_cat(cat: CatCreate, db: AsyncSession = Depends(get_db)) -> CatResponse:
    try:
        return await CatService.create_cat(db, cat)
    except Exception as e:
        logger.error(f"猫作成エラー: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/", response_model=CatAllResponse)
async def get_all_cats(db: AsyncSession = Depends(get_db)) -> CatAllResponse:
    try:
        return await CatService.get_all_cats(db)
    except Exception as e:
        logger.error(f"猫取得エラー: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{cat_id}", response_model=CatResponse)
async def get_cat(cat_id: str, db: AsyncSession = Depends(get_db)) -> CatResponse:
    try:
        return await CatService.get_cat_by_id(db, cat_id)
    except ValueError as e:
        logger.error(f"猫が見つかりません: {str(e)}")
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"猫取得エラー: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{cat_id}", response_model=UpdateCatResponse)
async def update_cat(
    cat_id: str, request: UpdateCatRequest, db: AsyncSession = Depends(get_db)
) -> UpdateCatResponse:
    try:
        return await CatService.update_cat(cat_id, request, db)
    except ValueError as e:
        logger.error(f"猫が見つかりません: {str(e)}")
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"猫更新エラー: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{cat_id}", response_model=DeleteCatResponse)
async def delete_cat(
    cat_id: str, db: AsyncSession = Depends(get_db)
) -> DeleteCatResponse:
    try:
        return await CatService.delete_cat(cat_id, db)
    except ValueError as e:
        logger.error(f"猫が見つかりません: {str(e)}")
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"猫削除エラー: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))