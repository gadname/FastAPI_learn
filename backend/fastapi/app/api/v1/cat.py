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


@router.post("/", response_model=CatResponse, summary="新しい猫を作成")
async def create_cat(cat: CatCreate, db: AsyncSession = Depends(get_db)) -> CatResponse:
    """
    新しい猫を作成します。
    
    Args:
        cat: 作成する猫の情報（名前、品種、年齢、体重）
        db: データベースセッション
    
    Returns:
        CatResponse: 作成された猫の情報（ID、作成日時を含む）
    
    Raises:
        HTTPException: 猫の作成に失敗した場合（500エラー）
    """
    try:
        return await CatService.create_cat(db, cat)
    except Exception as e:
        logger.error(f"猫作成エラー: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/", response_model=CatAllResponse, summary="全ての猫を取得")
async def get_all_cats(db: AsyncSession = Depends(get_db)) -> CatAllResponse:
    """
    データベースに登録されている全ての猫を取得します。
    
    Args:
        db: データベースセッション
    
    Returns:
        CatAllResponse: 全ての猫のリスト
    
    Raises:
        HTTPException: 猫の取得に失敗した場合（500エラー）
    """
    try:
        return await CatService.get_all_cats(db)
    except Exception as e:
        logger.error(f"猫取得エラー: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{cat_id}", response_model=CatResponse, summary="特定の猫を取得")
async def get_cat(cat_id: str, db: AsyncSession = Depends(get_db)) -> CatResponse:
    """
    指定されたIDの猫を取得します。
    
    Args:
        cat_id: 取得する猫のID
        db: データベースセッション
    
    Returns:
        CatResponse: 指定されたIDの猫の情報
    
    Raises:
        HTTPException: 猫が見つからない場合（404エラー）または取得に失敗した場合（500エラー）
    """
    try:
        return await CatService.get_cat_by_id(db, cat_id)
    except ValueError as e:
        logger.error(f"猫が見つかりません: {str(e)}")
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"猫取得エラー: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{cat_id}", response_model=UpdateCatResponse, summary="猫の情報を更新")
async def update_cat(
    cat_id: str, request: UpdateCatRequest, db: AsyncSession = Depends(get_db)
) -> UpdateCatResponse:
    """
    指定されたIDの猫の情報を更新します。
    
    Args:
        cat_id: 更新する猫のID
        request: 更新する情報（名前、品種、年齢、体重）
        db: データベースセッション
    
    Returns:
        UpdateCatResponse: 更新された猫の情報
    
    Raises:
        HTTPException: 猫が見つからない場合（404エラー）または更新に失敗した場合（500エラー）
    """
    try:
        return await CatService.update_cat(cat_id, request, db)
    except ValueError as e:
        logger.error(f"猫が見つかりません: {str(e)}")
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"猫更新エラー: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{cat_id}", response_model=DeleteCatResponse, summary="猫を削除")
async def delete_cat(
    cat_id: str, db: AsyncSession = Depends(get_db)
) -> DeleteCatResponse:
    """
    指定されたIDの猫を削除します。
    
    Args:
        cat_id: 削除する猫のID
        db: データベースセッション
    
    Returns:
        DeleteCatResponse: 削除結果のメッセージと削除された猫のID
    
    Raises:
        HTTPException: 猫が見つからない場合（404エラー）または削除に失敗した場合（500エラー）
    """
    try:
        return await CatService.delete_cat(cat_id, db)
    except ValueError as e:
        logger.error(f"猫が見つかりません: {str(e)}")
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"猫削除エラー: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))