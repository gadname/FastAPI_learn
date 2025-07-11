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

# Create router using base CRUD router
crud_router = BaseCRUDRouter(
    prefix="/bot",
    tags=["bot"],
    service=ChatBotService,
    create_schema=BotCreate,
    response_schema=BotResponse,
    update_schema=UpdateBotRequest,
    all_response_schema=BotAllResponse,
    delete_response_schema=DeleteBotResponse,
    resource_name="ボット"
)

# Export the router
router = crud_router.router
