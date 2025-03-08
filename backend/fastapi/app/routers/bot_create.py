from fastapi import APIRouter, Depends
from app.db.cruds.character import create_character_service
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.bot import BotCreate, BotResponse
from app.db.database import get_db
from fastapi import HTTPException
from app.utils.logging import logger

router = APIRouter(prefix="/bot", tags=["bot"])


@router.post("/", response_model=BotResponse)
async def create_bot(bot: BotCreate, db: AsyncSession = Depends(get_db)) -> BotResponse:
    try:
        return await create_bot_service(bot, db)
    except Exception as e:
        # 開発者用のログ
        logger.error(f"ボット作成エラー: {str(e)}")
        # ユーザー用のログ
        raise HTTPException(status_code=500, detail=str(e))
