from app.models.chat_bot import ChatBot
from app.schemas.bot import (
    BotCreate,
    BotResponse,
    BotAllResponse,
    UpdateBotResponse,
    UpdateBotRequest,
    DeleteBotResponse,
)
from app.services.base.base_service import BaseService


class ChatBotService(BaseService[
    ChatBot,
    BotCreate,
    BotResponse,
    BotAllResponse,
    UpdateBotRequest,
    UpdateBotResponse,
    DeleteBotResponse
]):
    def __init__(self):
        super().__init__(
            model=ChatBot,
            response_schema=BotResponse,
            all_response_schema=BotAllResponse,
            update_response_schema=UpdateBotResponse,
            delete_response_schema=DeleteBotResponse,
            entity_name="ボット",
            entity_name_plural="bots"
        )
    
    # Legacy methods for backward compatibility
    @classmethod
    async def create_chat_bot(cls, session, bot):
        """Legacy method for backward compatibility"""
        return await cls.create_entity(session, bot)
    
    @classmethod
    async def get_all_bots(cls, session):
        """Legacy method for backward compatibility"""
        return await cls.get_all_entities(session)
    
    @classmethod
    async def get_bot_by_id(cls, session, bot_id):
        """Legacy method for backward compatibility"""
        return await cls.get_entity_by_id(session, bot_id)
    
    @classmethod
    async def update_bot(cls, bot_id, request, session):
        """Legacy method for backward compatibility"""
        return await cls.update_entity(bot_id, request, session)
    
    @classmethod
    async def delete_bot(cls, bot_id, session):
        """Legacy method for backward compatibility"""
        return await cls.delete_entity(bot_id, session)
