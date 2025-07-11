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
from app.services.base.base_service import LegacyServiceAdapter

# Create a router instance using the base CRUD router
bot_router = BaseCRUDRouter(
    prefix="/bot",
    tags=["bot"],
    service_class=LegacyServiceAdapter(ChatBotService),
    create_schema=BotCreate,
    response_schema=BotResponse,
    all_response_schema=BotAllResponse,
    update_request_schema=UpdateBotRequest,
    update_response_schema=UpdateBotResponse,
    delete_response_schema=DeleteBotResponse,
    entity_name="chat_bot",
    entity_name_jp="ボット",
    service_method_names={
        "create": "create_chat_bot",
        "get_all": "get_all_bots",
        "get_by_id": "get_bot_by_id",
        "update": "update_bot",
        "delete": "delete_bot",
    },
)

# Export the router
router = bot_router.router
