from fastapi import APIRouter
from .bot import router as bot_router
from .cat import router as cat_router
from .auth import router as auth_router

v1_router = APIRouter()

v1_router.include_router(bot_router, prefix="/bot", tags=["bot"])
v1_router.include_router(cat_router, prefix="/cat", tags=["cat"])
v1_router.include_router(auth_router, prefix="/auth", tags=["auth"])
