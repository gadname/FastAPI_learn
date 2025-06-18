from fastapi import APIRouter
from .bot import router as bot_router
from .cat import router as cat_router
from .dog import router as dog_router

api_router = APIRouter()

api_router.include_router(bot_router)
api_router.include_router(cat_router)
api_router.include_router(dog_router)
