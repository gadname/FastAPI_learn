from fastapi import APIRouter, Depends
from fastapi import HTTPException

from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.bot import (
    BotCreate,
    BotResponse,
    BotAllResponse,
    UpdateBotResponse,
    UpdateBotRequest,
    DeleteBotResponse,
)

from app.db.database import get_db
from app.services.chat_bot import ChatBotService
from app.utils.logging import logger


router = APIRouter(prefix="/bot", tags=["bot"])


@router.post("/", response_model=BotResponse, summary="新しいボットを作成")
async def create_bot(bot: BotCreate, db: AsyncSession = Depends(get_db)) -> BotResponse:
    """
    新しいチャットボットを作成します。
    
    Args:
        bot: 作成するボットの情報（名前、色）
        db: データベースセッション
    
    Returns:
        BotResponse: 作成されたボットの情報（ID、作成日時を含む）
    
    Raises:
        HTTPException: ボットの作成に失敗した場合（500エラー）
    """
    try:
        return await ChatBotService.create_chat_bot(db, bot)
    except Exception as e:
        logger.error(f"ボット作成エラー: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/", response_model=BotAllResponse, summary="全てのボットを取得")
async def get_all_bots(db: AsyncSession = Depends(get_db)) -> BotAllResponse:
    """
    データベースに登録されている全てのチャットボットを取得します。
    
    Args:
        db: データベースセッション
    
    Returns:
        BotAllResponse: 全てのチャットボットのリスト
    
    Raises:
        HTTPException: ボットの取得に失敗した場合（500エラー）
    """
    try:
        return await ChatBotService.get_all_bots(db)
    except Exception as e:
        logger.error(f"ボット取得エラー: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{bot_id}", response_model=BotResponse, summary="特定のボットを取得")
async def get_bot(bot_id: str, db: AsyncSession = Depends(get_db)) -> BotResponse:
    """
    指定されたIDのチャットボットを取得します。
    
    Args:
        bot_id: 取得するボットのID
        db: データベースセッション
    
    Returns:
        BotResponse: 指定されたIDのチャットボットの情報
    
    Raises:
        HTTPException: ボットが見つからない場合（404エラー）または取得に失敗した場合（500エラー）
    """
    try:
        return await ChatBotService.get_bot_by_id(db, bot_id)
    except ValueError as e:
        logger.error(f"ボットが見つかりません: {str(e)}")
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"ボット取得エラー: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{bot_id}", response_model=UpdateBotResponse, summary="ボットの情報を更新")
async def update_bot(
    bot_id: str, request: UpdateBotRequest, db: AsyncSession = Depends(get_db)
) -> UpdateBotResponse:
    """
    指定されたIDのチャットボットの情報を更新します。
    
    Args:
        bot_id: 更新するボットのID
        request: 更新する情報（名前、色）
        db: データベースセッション
    
    Returns:
        UpdateBotResponse: 更新されたチャットボットの情報
    
    Raises:
        HTTPException: ボットが見つからない場合（404エラー）または更新に失敗した場合（500エラー）
    """
    try:
        return await ChatBotService.update_bot(bot_id, request, db)
    except ValueError as e:
        logger.error(f"ボットが見つかりません: {str(e)}")
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"ボット更新エラー: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{bot_id}", response_model=DeleteBotResponse, summary="ボットを削除")
async def delete_bot(
    bot_id: str, db: AsyncSession = Depends(get_db)
) -> DeleteBotResponse:
    """
    指定されたIDのチャットボットを削除します。
    
    Args:
        bot_id: 削除するボットのID
        db: データベースセッション
    
    Returns:
        DeleteBotResponse: 削除結果のメッセージと削除されたボットのID
    
    Raises:
        HTTPException: ボットが見つからない場合（404エラー）または削除に失敗した場合（500エラー）
    """
    try:
        return await ChatBotService.delete_bot(bot_id, db)
    except ValueError as e:
        logger.error(f"ボットが見つかりません: {str(e)}")
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"ボット削除エラー: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
