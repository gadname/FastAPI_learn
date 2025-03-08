from sqlalchemy.ext.asyncio import AsyncSession

from app.models.chat_bot import ChatBot
from app.schemas.bot import BotCreate


class ChatBotCRUD:
    @staticmethod
    async def create_chat_bot(
        session: AsyncSession,
        bot: BotCreate,
    ) -> ChatBot:
        new_bot = ChatBot(
            name=bot.name,
            color=bot.color,
        )
        session.add(new_bot)
        await session.flush()
        await session.refresh(new_bot)
        return new_bot
