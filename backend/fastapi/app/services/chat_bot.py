from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.bot import (
    BotCreate,
    BotResponse,
    BotAllResponse,
    UpdateBotResponse,
    UpdateBotRequest,
)
from app.cruds.chat_bot import ChatBotCRUD


class ChatBotService:
    @staticmethod
    async def create_chat_bot(
        session: AsyncSession,
        bot: BotCreate,
    ) -> BotResponse:
        try:
            bot_data = await ChatBotCRUD.create_chat_bot(session, bot)
            return bot_data
        except Exception as e:
            raise e

    @staticmethod
    async def get_all_bots(session: AsyncSession) -> BotAllResponse:
        try:
            bots = await ChatBotCRUD.get_all_bots(session)
            return BotAllResponse(bots=bots)
        except Exception as e:
            raise e

    @staticmethod
    async def update_bot(
        bot_id: str, request: UpdateBotRequest, session: AsyncSession
    ) -> UpdateBotResponse:
        try:
            async with session.begin():
                update_bot = await ChatBotCRUD.update_bot(
                    bot_id=bot_id,
                    session=session,
                    name=request.name,
                    color=request.color,
                )
                return update_bot
        except Exception as e:
            raise e
