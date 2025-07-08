from app.api.base.base_router import BaseCRUDRouter
from app.schemas.bot import (
    BotCreate,
    BotResponse,
    BotAllResponse,
    UpdateBotResponse,
    UpdateBotRequest,
    DeleteBotResponse,
)
from app.services.chat_bot import ChatBotService

# Create the router using the base CRUD router
bot_router = BaseCRUDRouter[
    BotCreate,
    BotResponse,
    BotAllResponse,
    UpdateBotRequest,
    UpdateBotResponse,
    DeleteBotResponse
](
    prefix="/bot",
    tags=["bot"],
    service_class=ChatBotService,
    create_schema=BotCreate,
    response_schema=BotResponse,
    all_response_schema=BotAllResponse,
    update_request_schema=UpdateBotRequest,
    update_response_schema=UpdateBotResponse,
    delete_response_schema=DeleteBotResponse,
    entity_name="ボット"
)

# Export the router
router = bot_router.router
