from supabase import create_client, Client
from app.settings import settings
from app.utils.logging import logger
from typing import Optional

# Supabaseクライアントのインスタンス
supabase_client: Optional[Client] = None


def get_supabase_client() -> Optional[Client]:
    """
    Supabaseクライアントのインスタンスを取得
    設定でuse_supabaseがTrueの場合のみ初期化
    """
    global supabase_client
    
    if not settings.use_supabase:
        logger.info("Supabase is disabled. Using traditional PostgreSQL connection.")
        return None
    
    if supabase_client is None:
        if not settings.supabase_url or not settings.supabase_key:
            logger.error("Supabase URL or Key is not configured properly.")
            return None
        
        try:
            supabase_client = create_client(
                settings.supabase_url,
                settings.supabase_key
            )
            logger.info("Supabase client initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Supabase client: {e}")
            return None
    
    return supabase_client


def get_supabase_service_client() -> Optional[Client]:
    """
    Supabaseサービスロールクライアントのインスタンスを取得
    管理者権限が必要な操作用
    """
    if not settings.use_supabase:
        return None
    
    if not settings.supabase_url or not settings.supabase_service_role_key:
        logger.error("Supabase URL or Service Role Key is not configured properly.")
        return None
    
    try:
        service_client = create_client(
            settings.supabase_url,
            settings.supabase_service_role_key
        )
        logger.info("Supabase service client initialized successfully")
        return service_client
    except Exception as e:
        logger.error(f"Failed to initialize Supabase service client: {e}")
        return None


def test_supabase_connection() -> bool:
    """
    Supabase接続をテスト
    """
    client = get_supabase_client()
    if not client:
        return False
    
    try:
        # Simple test query
        result = client.table('chat_bots').select('*').limit(1).execute()
        logger.info("Supabase connection test successful")
        return True
    except Exception as e:
        logger.error(f"Supabase connection test failed: {e}")
        return False