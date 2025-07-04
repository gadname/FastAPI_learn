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
from app.utils.logging import logger # Ensure logger is imported if not already
from app.api.v1.base_router import generic_router_factory # Corrected import name

# Adapter class to bridge ChatBotService and generic_router_factory
class ChatBotServiceAdapter:
    async def create(self, db: AsyncSession, obj_in: BotCreate) -> BotResponse:
        # Note: ChatBotService.create_chat_bot returns BotResponse which matches
        return await ChatBotService.create_chat_bot(session=db, bot=obj_in)

    async def get_multi(self, db: AsyncSession, skip: int = 0, limit: int = 100) -> BotAllResponse: # Changed return type to BotAllResponse
        # ChatBotService.get_all_bots doesn't support pagination (skip, limit).
        # It directly returns BotAllResponse.
        # We call it and ignore skip/limit for now.
        # If pagination is critical, ChatBotService.get_all_bots would need modification.
        return await ChatBotService.get_all_bots(session=db) # Return the direct response

    async def get(self, db: AsyncSession, id: str) -> BotResponse:
        # ChatBotService.get_bot_by_id returns BotResponse
        return await ChatBotService.get_bot_by_id(session=db, bot_id=id)

    async def update(self, db: AsyncSession, db_obj: BotResponse, obj_in: UpdateBotRequest) -> UpdateBotResponse:
        # generic_router_factory first fetches the object (db_obj), then passes it to update.
        # ChatBotService.update_bot needs bot_id and the request schema.
        # Assuming db_obj has an 'id' attribute.
        if not hasattr(db_obj, 'id'):
            # This case should ideally not happen if db_obj is a BotResponse model from get()
            raise ValueError("db_obj must have an id attribute for update")
        return await ChatBotService.update_bot(bot_id=db_obj.id, request=obj_in, session=db)

    async def remove(self, db: AsyncSession, id: str) -> DeleteBotResponse:
        # ChatBotService.delete_bot returns DeleteBotResponse
        return await ChatBotService.delete_bot(bot_id=id, session=db)

# Instantiate the adapter
adapted_chatbot_service = ChatBotServiceAdapter()

# Create the router using the generic factory and the adapter
router = generic_router_factory(
    service=adapted_chatbot_service,
    tags=["bot"],
    prefix="/bot",
    response_model=BotResponse,
    create_schema=BotCreate,
    update_schema=UpdateBotRequest,
    get_all_response_model=BotAllResponse, # Changed back to BotAllResponse
    update_response_model=UpdateBotResponse,
    delete_response_model=DeleteBotResponse,
)
