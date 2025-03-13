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


@router.post("/", response_model=BotResponse)
async def create_bot(bot: BotCreate, db: AsyncSession = Depends(get_db)) -> BotResponse:
    try:
        return await ChatBotService.create_chat_bot(db, bot)
    except Exception as e:
        logger.error(f"ボット作成エラー: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/", response_model=BotAllResponse)
async def get_all_bots(db: AsyncSession = Depends(get_db)) -> BotAllResponse:
    try:
        return await ChatBotService.get_all_bots(db)
    except Exception as e:
        logger.error(f"ボット取得エラー: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{bot_id}", response_model=UpdateBotResponse)
async def update_bot(
    bot_id: str, request: UpdateBotRequest, db: AsyncSession = Depends(get_db)
) -> UpdateBotResponse:
    try:
        return await ChatBotService.update_bot(bot_id, request, db)
    except Exception as e:
        logger.error(f"ボット更新エラー: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{bot_id}", response_model=DeleteBotResponse)
async def delete_bot(
    bot_id: str, db: AsyncSession = Depends(get_db)
) -> DeleteBotResponse:
    try:
        return await ChatBotService.delete_bot(bot_id, db)
    except Exception as e:
        logger.error(f"ボット削除エラー")
        raise HTTPException(status_code=500, detail=str(e))
