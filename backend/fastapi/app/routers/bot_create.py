from fastapi import APIRouter, Depends
from fastapi import HTTPException

from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.bot import BotCreate, BotResponse

from app.db.database import get_db
from app.services.chat_bot import create_chat_bot

from app.utils.logging import logger

router = APIRouter(prefix="/bot", tags=["bot"])


@router.post("/", response_model=BotResponse)
async def create_bot(bot: BotCreate, db: AsyncSession = Depends(get_db)) -> BotResponse:
    try:
        return await create_chat_bot(bot, db)
    except Exception as e:
        logger.error(f"ボット作成エラー: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
