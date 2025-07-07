from typing import Optional, Dict, Any
from fastapi import HTTPException, Depends, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.db.supabase_client import get_supabase_client
from app.utils.logging import logger
from app.settings import settings
import jwt
from datetime import datetime, timezone


# JWT Bearer認証スキーム
security = HTTPBearer()


class AuthService:
    """
    Supabase認証サービス
    """
    
    def __init__(self):
        self.supabase_client = get_supabase_client()
    
    def verify_token(self, token: str) -> Optional[Dict[str, Any]]:
        """
        Supabase JWTトークンを検証
        """
        if not self.supabase_client or not settings.use_supabase:
            logger.warning("Supabase auth is not enabled")
            return None
        
        try:
            # Note: この実装は簡易版です。
            # 実際のプロダクションでは、Supabaseのサーバーサイド認証を使用する必要があります
            
            # トークンをデコード (検証なし - 開発用)
            payload = jwt.decode(token, options={"verify_signature": False})
            
            # 有効期限をチェック
            if 'exp' in payload:
                exp_timestamp = payload['exp']
                if datetime.now(timezone.utc).timestamp() > exp_timestamp:
                    logger.warning("Token has expired")
                    return None
            
            return payload
            
        except Exception as e:
            logger.error(f"Token verification failed: {e}")
            return None
    
    def get_current_user(self, token: str) -> Optional[Dict[str, Any]]:
        """
        現在のユーザー情報を取得
        """
        payload = self.verify_token(token)
        if not payload:
            return None
        
        return {
            "id": payload.get("sub"),
            "email": payload.get("email"),
            "role": payload.get("role", "user"),
            "aud": payload.get("aud"),
            "exp": payload.get("exp")
        }


# 認証サービスのインスタンス
auth_service = AuthService()


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> Optional[Dict[str, Any]]:
    """
    現在のユーザーを取得 (依存関数)
    """
    if not settings.use_supabase:
        # Supabaseが無効の場合、認証をスキップ
        logger.info("Supabase auth is disabled. Skipping authentication.")
        return None
    
    try:
        token = credentials.credentials
        user = auth_service.get_current_user(token)
        
        if not user:
            raise HTTPException(
                status_code=401,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        return user
    except Exception as e:
        logger.error(f"Authentication failed: {e}")
        raise HTTPException(
            status_code=401,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


def get_optional_user(credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)) -> Optional[Dict[str, Any]]:
    """
    オプショナルなユーザー取得 (認証が必須でない場合)
    """
    if not credentials or not settings.use_supabase:
        return None
    
    try:
        token = credentials.credentials
        return auth_service.get_current_user(token)
    except:
        return None


def require_admin(user: Dict[str, Any] = Depends(get_current_user)) -> Dict[str, Any]:
    """
    管理者権限が必要な場合の依存関数
    """
    if not user or user.get("role") != "admin":
        raise HTTPException(
            status_code=403,
            detail="Admin privileges required"
        )
    
    return user