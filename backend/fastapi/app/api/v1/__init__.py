from fastapi import APIRouter
from .bot import router as bot_router
from .cat import router as cat_router

v1_router = APIRouter()

v1_router.include_router(bot_router)
v1_router.include_router(cat_router)
