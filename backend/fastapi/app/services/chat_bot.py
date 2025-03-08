from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.bot import BotCreate, BotResponse
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
