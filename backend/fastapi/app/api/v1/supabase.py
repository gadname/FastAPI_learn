from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Dict, Any, Optional
from app.services.auth import get_current_user, get_optional_user
from app.services.hybrid_db import hybrid_db
from app.db.supabase_client import get_supabase_client, test_supabase_connection
from app.settings import settings
from pydantic import BaseModel
from app.utils.logging import logger

router = APIRouter()


class SupabaseStatus(BaseModel):
    enabled: bool
    url: str
    connected: bool
    message: str


class ChatBotCreate(BaseModel):
    name: str
    color: str


class CatCreate(BaseModel):
    name: str
    breed: Optional[str] = None
    age: Optional[int] = None
    weight: Optional[float] = None


@router.get("/status", response_model=SupabaseStatus)
async def get_supabase_status():
    """
    Supabaseの接続状態を確認
    """
    try:
        client = get_supabase_client()
        is_connected = False
        message = "Supabase is not configured"
        
        if settings.use_supabase and client:
            is_connected = test_supabase_connection()
            message = "Supabase is connected and ready" if is_connected else "Supabase configuration exists but connection failed"
        elif not settings.use_supabase:
            message = "Supabase is disabled in settings"
        
        return SupabaseStatus(
            enabled=settings.use_supabase,
            url=settings.supabase_url if settings.supabase_url else "Not configured",
            connected=is_connected,
            message=message
        )
    except Exception as e:
        logger.error(f"Error checking Supabase status: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to check Supabase status: {str(e)}"
        )


@router.get("/chat-bots", response_model=List[Dict[str, Any]])
async def get_chat_bots_supabase(
    user: Optional[Dict[str, Any]] = Depends(get_optional_user)
):
    """
    チャットボット一覧を取得 (Supabase/SQLAlchemy ハイブリッド)
    """
    try:
        chat_bots = await hybrid_db.get_chat_bots()
        
        # 認証されたユーザーの場合、追加情報を提供
        if user:
            logger.info(f"Authenticated user {user.get('email')} accessed chat bots")
        
        return chat_bots
    except Exception as e:
        logger.error(f"Error fetching chat bots: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch chat bots: {str(e)}"
        )


@router.post("/chat-bots", response_model=Dict[str, Any])
async def create_chat_bot_supabase(
    chat_bot: ChatBotCreate,
    user: Optional[Dict[str, Any]] = Depends(get_optional_user)
):
    """
    チャットボットを作成 (Supabase/SQLAlchemy ハイブリッド)
    """
    try:
        chat_bot_data = {
            "name": chat_bot.name,
            "color": chat_bot.color
        }
        
        # 認証されたユーザーの場合、作成者情報を追加
        if user:
            chat_bot_data["created_by"] = user.get("id")
            logger.info(f"User {user.get('email')} creating chat bot: {chat_bot.name}")
        
        new_chat_bot = await hybrid_db.create_chat_bot(chat_bot_data)
        return new_chat_bot
    except Exception as e:
        logger.error(f"Error creating chat bot: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create chat bot: {str(e)}"
        )


@router.get("/cats", response_model=List[Dict[str, Any]])
async def get_cats_supabase(
    user: Optional[Dict[str, Any]] = Depends(get_optional_user)
):
    """
    猫一覧を取得 (Supabase/SQLAlchemy ハイブリッド)
    """
    try:
        cats = await hybrid_db.get_cats()
        
        # 認証されたユーザーの場合、追加情報を提供
        if user:
            logger.info(f"Authenticated user {user.get('email')} accessed cats")
        
        return cats
    except Exception as e:
        logger.error(f"Error fetching cats: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch cats: {str(e)}"
        )


@router.post("/cats", response_model=Dict[str, Any])
async def create_cat_supabase(
    cat: CatCreate,
    user: Optional[Dict[str, Any]] = Depends(get_optional_user)
):
    """
    猫を作成 (Supabase/SQLAlchemy ハイブリッド)
    """
    try:
        cat_data = {
            "name": cat.name,
            "breed": cat.breed,
            "age": cat.age,
            "weight": cat.weight
        }
        
        # 認証されたユーザーの場合、作成者情報を追加
        if user:
            cat_data["created_by"] = user.get("id")
            logger.info(f"User {user.get('email')} creating cat: {cat.name}")
        
        new_cat = await hybrid_db.create_cat(cat_data)
        return new_cat
    except Exception as e:
        logger.error(f"Error creating cat: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create cat: {str(e)}"
        )