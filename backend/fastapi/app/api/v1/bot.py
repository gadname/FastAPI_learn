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
from app.models.chat_bot import ChatBot


# Create CRUD router instance using the base class
bot_router = BaseCRUDRouter(
    prefix="/bot",
    tags=["bot"],
    service_class=ChatBotService,
    response_model=BotResponse,
    all_response_model=BotAllResponse,
    update_response_model=UpdateBotResponse,
    delete_response_model=DeleteBotResponse,
    resource_name="bot",
    resource_name_ja="ボット",
    use_legacy_adapter=True,
)

# Export the router
router = bot_router.get_router()
