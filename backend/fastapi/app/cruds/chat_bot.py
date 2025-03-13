from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
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
        await session.commit()
        return new_bot

    @staticmethod
    async def get_all_bots(session: AsyncSession) -> list[ChatBot]:
        bots = await session.execute(select(ChatBot))
        return bots.scalars().all()

    @staticmethod
    async def update_bot(bot_id: str, session: AsyncSession, **kwargs) -> ChatBot:
        await session.execute(
            update(ChatBot).where(ChatBot.id == bot_id).values(**kwargs)
        )
        await session.flush()
        return await ChatBotCRUD.get_bot_by_id(bot_id, session)

    @staticmethod
    async def get_bot_by_id(bot_id: str, session: AsyncSession) -> ChatBot:
        result = await session.execute(select(ChatBot).where(ChatBot.id == bot_id))
        bot = result.scalars().one_or_none()
        return bot

    @staticmethod
    async def delete_bot(bot_id: str, session: AsyncSession) -> ChatBot:
        result = await session.execute(select(ChatBot).where(ChatBot.id == bot_id))
        bot = result.scalars().one_or_none()
        await session.delete(bot)
        return bot
