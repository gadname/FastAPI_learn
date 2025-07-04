from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.bot import (
    BotCreate,
    BotResponse,
    BotAllResponse,
    UpdateBotResponse,
    UpdateBotRequest,
    DeleteBotResponse,
)
from app.cruds.chat_bot import ChatBotCRUD
from app.utils.logging import logger


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
            logger.error(f"ボット作成中にエラーが発生しました: {str(e)}")
            raise e

    @staticmethod
    async def get_all_bots(session: AsyncSession) -> BotAllResponse:
        try:
            bots = await ChatBotCRUD.get_all_bots(session)
            return BotAllResponse(bots=bots)
        except Exception as e:
            logger.error(f"ボット取得中にエラーが発生しました: {str(e)}")
            raise e

    @staticmethod
    async def get_bot_by_id(session: AsyncSession, bot_id: str) -> BotResponse:
        try:
            bot = await ChatBotCRUD.get_bot_by_id(bot_id, session)
            if not bot:
                raise ValueError(f"ID {bot_id} のボットが見つかりません")
            return BotResponse.model_validate(bot)
        except Exception as e:
            logger.error(f"ボット取得中にエラーが発生しました: {str(e)}")
            raise e

    @staticmethod
    async def update_bot(
        bot_id: str, request: UpdateBotRequest, session: AsyncSession
    ) -> UpdateBotResponse:
        try:
            # ボットの存在確認
            bot = await ChatBotCRUD.get_bot_by_id(bot_id, session)
            if not bot:
                raise ValueError(f"ID {bot_id} のボットが見つかりません")

            # Only update fields that are provided
            update_data = {}
            if request.name is not None:
                update_data["name"] = request.name
            if request.color is not None:
                update_data["color"] = request.color

            if not update_data:
                # No updates requested, return current bot
                return UpdateBotResponse.model_validate(bot)

            update_bot = await ChatBotCRUD.update_bot(
                bot_id=bot_id, session=session, **update_data
            )
            return update_bot
        except ValueError as e:
            raise e
        except Exception as e:
            logger.error(f"ボット更新中にエラーが発生しました: {str(e)}")
            raise e

    @staticmethod
    async def delete_bot(bot_id: str, session: AsyncSession) -> DeleteBotResponse:
        try:
            # ボットの存在確認
            bot = await ChatBotCRUD.get_bot_by_id(bot_id, session)
            if not bot:
                raise ValueError(f"ID {bot_id} のボットが見つかりません")

            await ChatBotCRUD.delete_bot(bot_id=bot_id, session=session)
            return DeleteBotResponse(id=bot_id)
        except ValueError as e:
            raise e
        except Exception as e:
            logger.error(f"ボット削除中にエラーが発生しました: {str(e)}")
            raise e
