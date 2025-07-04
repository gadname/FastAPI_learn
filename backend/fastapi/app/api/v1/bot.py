from fastapi import APIRouter, Depends
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
from app.utils.router_utils import (
    handle_create_operation,
    handle_get_operation,
    handle_update_operation,
    handle_delete_operation,
)


router = APIRouter(prefix="/bot", tags=["bot"])


@router.post("/", response_model=BotResponse)
@handle_create_operation("ボット")
async def create_bot(bot: BotCreate, db: AsyncSession = Depends(get_db)) -> BotResponse:
    return await ChatBotService.create_chat_bot(db, bot)


@router.get("/", response_model=BotAllResponse)
@handle_get_operation("ボット")
async def get_all_bots(db: AsyncSession = Depends(get_db)) -> BotAllResponse:
    return await ChatBotService.get_all_bots(db)


@router.get("/{bot_id}", response_model=BotResponse)
@handle_get_operation("ボット")
async def get_bot(bot_id: str, db: AsyncSession = Depends(get_db)) -> BotResponse:
    return await ChatBotService.get_bot_by_id(db, bot_id)


@router.put("/{bot_id}", response_model=UpdateBotResponse)
@handle_update_operation("ボット")
async def update_bot(
    bot_id: str, request: UpdateBotRequest, db: AsyncSession = Depends(get_db)
) -> UpdateBotResponse:
    return await ChatBotService.update_bot(bot_id, request, db)


@router.delete("/{bot_id}", response_model=DeleteBotResponse)
@handle_delete_operation("ボット")
async def delete_bot(
    bot_id: str, db: AsyncSession = Depends(get_db)
) -> DeleteBotResponse:
    return await ChatBotService.delete_bot(bot_id, db)
