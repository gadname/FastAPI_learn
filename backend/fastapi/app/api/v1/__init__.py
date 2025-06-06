from fastapi import APIRouter
from .bot import router as bot_router
from .endpoints.adv_chat import router as adv_chat_router

v1_router = APIRouter()

v1_router.include_router(bot_router)
v1_router.include_router(adv_chat_router)
