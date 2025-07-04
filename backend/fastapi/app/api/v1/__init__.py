from fastapi import APIRouter
from .bot import router as bot_router
from .cat import router as cat_router

# Central router configuration
v1_router = APIRouter()

# Include all sub-routers with consistent configuration
v1_router.include_router(bot_router, prefix="", tags=["v1"])
v1_router.include_router(cat_router, prefix="", tags=["v1"])
