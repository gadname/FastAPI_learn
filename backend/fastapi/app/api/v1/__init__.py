from fastapi import APIRouter

# Assuming other routers like bot_router and cat_router are defined in bot.py and cat.py
from .bot import router as bot_router
from .cat import router as cat_router
from .auth import router as auth_router # Import the new auth router

v1_router = APIRouter()
v1_router.include_router(bot_router, prefix="/bot", tags=["Bot"])
v1_router.include_router(cat_router, prefix="/cats", tags=["Cats"])
v1_router.include_router(auth_router, prefix="/auth", tags=["Authentication"]) # Add the auth router
