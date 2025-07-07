from typing import List, Optional, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.supabase_client import get_supabase_client
from app.settings import settings
from app.utils.logging import logger


class HybridDBService:
    """
    従来のSQLAlchemyとSupabaseの両方をサポートするハイブリッドDBサービス
    """
    
    def __init__(self):
        self.supabase_client = get_supabase_client()
        self.use_supabase = settings.use_supabase and self.supabase_client is not None
        
        if self.use_supabase:
            logger.info("Using Supabase for database operations")
        else:
            logger.info("Using traditional SQLAlchemy for database operations")
    
    async def get_chat_bots(self, db: Optional[AsyncSession] = None) -> List[Dict[str, Any]]:
        """
        チャットボット一覧を取得
        """
        if self.use_supabase:
            try:
                response = self.supabase_client.table('chat_bots').select('*').order('created_at', desc=True).execute()
                return response.data
            except Exception as e:
                logger.error(f"Supabase query failed: {e}")
                # フォールバックとして従来のSQLAlchemyを使用
                if db:
                    return await self._get_chat_bots_sqlalchemy(db)
                else:
                    return []
        else:
            if db:
                return await self._get_chat_bots_sqlalchemy(db)
            else:
                return []
    
    async def _get_chat_bots_sqlalchemy(self, db: AsyncSession) -> List[Dict[str, Any]]:
        """
        SQLAlchemyを使用してチャットボットを取得
        """
        if not db:
            raise ValueError("Database session is required for SQLAlchemy operations")
        
        from app.models.chat_bot import ChatBot
        from sqlalchemy import select
        
        result = await db.execute(select(ChatBot).order_by(ChatBot.created_at.desc()))
        chat_bots = result.scalars().all()
        
        return [
            {
                "id": bot.id,
                "name": bot.name,
                "color": bot.color,
                "created_at": bot.created_at.isoformat(),
                "updated_at": bot.updated_at.isoformat()
            }
            for bot in chat_bots
        ]
    
    async def create_chat_bot(self, data: Dict[str, Any], db: Optional[AsyncSession] = None) -> Dict[str, Any]:
        """
        チャットボットを作成
        """
        if self.use_supabase:
            try:
                response = self.supabase_client.table('chat_bots').insert(data).execute()
                return response.data[0] if response.data else {}
            except Exception as e:
                logger.error(f"Supabase insert failed: {e}")
                # フォールバックとして従来のSQLAlchemyを使用
                if db:
                    return await self._create_chat_bot_sqlalchemy(data, db)
                else:
                    raise ValueError("Database session is required for fallback operations")
        else:
            if db:
                return await self._create_chat_bot_sqlalchemy(data, db)
            else:
                raise ValueError("Database session is required for SQLAlchemy operations")
    
    async def _create_chat_bot_sqlalchemy(self, data: Dict[str, Any], db: AsyncSession) -> Dict[str, Any]:
        """
        SQLAlchemyを使用してチャットボットを作成
        """
        if not db:
            raise ValueError("Database session is required for SQLAlchemy operations")
        
        from app.models.chat_bot import ChatBot
        
        new_bot = ChatBot(
            name=data.get("name"),
            color=data.get("color")
        )
        
        db.add(new_bot)
        await db.commit()
        await db.refresh(new_bot)
        
        return {
            "id": new_bot.id,
            "name": new_bot.name,
            "color": new_bot.color,
            "created_at": new_bot.created_at.isoformat(),
            "updated_at": new_bot.updated_at.isoformat()
        }
    
    async def get_cats(self, db: Optional[AsyncSession] = None) -> List[Dict[str, Any]]:
        """
        猫一覧を取得
        """
        if self.use_supabase:
            try:
                response = self.supabase_client.table('cats').select('*').order('created_at', desc=True).execute()
                return response.data
            except Exception as e:
                logger.error(f"Supabase query failed: {e}")
                # フォールバックとして従来のSQLAlchemyを使用
                if db:
                    return await self._get_cats_sqlalchemy(db)
                else:
                    return []
        else:
            if db:
                return await self._get_cats_sqlalchemy(db)
            else:
                return []
    
    async def _get_cats_sqlalchemy(self, db: AsyncSession) -> List[Dict[str, Any]]:
        """
        SQLAlchemyを使用して猫を取得
        """
        if not db:
            raise ValueError("Database session is required for SQLAlchemy operations")
        
        from app.models.cat import Cat
        from sqlalchemy import select
        
        result = await db.execute(select(Cat).order_by(Cat.created_at.desc()))
        cats = result.scalars().all()
        
        return [
            {
                "id": cat.id,
                "name": cat.name,
                "breed": cat.breed,
                "age": cat.age,
                "weight": cat.weight,
                "created_at": cat.created_at.isoformat(),
                "updated_at": cat.updated_at.isoformat()
            }
            for cat in cats
        ]
    
    async def create_cat(self, data: Dict[str, Any], db: Optional[AsyncSession] = None) -> Dict[str, Any]:
        """
        猫を作成
        """
        if self.use_supabase:
            try:
                response = self.supabase_client.table('cats').insert(data).execute()
                return response.data[0] if response.data else {}
            except Exception as e:
                logger.error(f"Supabase insert failed: {e}")
                # フォールバックとして従来のSQLAlchemyを使用
                if db:
                    return await self._create_cat_sqlalchemy(data, db)
                else:
                    raise ValueError("Database session is required for fallback operations")
        else:
            if db:
                return await self._create_cat_sqlalchemy(data, db)
            else:
                raise ValueError("Database session is required for SQLAlchemy operations")
    
    async def _create_cat_sqlalchemy(self, data: Dict[str, Any], db: AsyncSession) -> Dict[str, Any]:
        """
        SQLAlchemyを使用して猫を作成
        """
        if not db:
            raise ValueError("Database session is required for SQLAlchemy operations")
        
        from app.models.cat import Cat
        
        new_cat = Cat(
            name=data.get("name"),
            breed=data.get("breed"),
            age=data.get("age"),
            weight=data.get("weight")
        )
        
        db.add(new_cat)
        await db.commit()
        await db.refresh(new_cat)
        
        return {
            "id": new_cat.id,
            "name": new_cat.name,
            "breed": new_cat.breed,
            "age": new_cat.age,
            "weight": new_cat.weight,
            "created_at": new_cat.created_at.isoformat(),
            "updated_at": new_cat.updated_at.isoformat()
        }


# ハイブリッドDBサービスのインスタンス
hybrid_db = HybridDBService()