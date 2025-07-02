from typing import Any, AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker
from app.settings import settings
from urllib.parse import quote_plus
from app.utils.logging import logger

ai_bot_db_user: str = settings.ai_bot_db_user
ai_bot_db_password: str = quote_plus(settings.ai_bot_db_password)
ai_bot_db_name: str = settings.ai_bot_db_name
ai_bot_db_host: str = settings.ai_bot_db_host
ai_bot_cloud_sql_connection_name: str = settings.ai_bot_cloud_sql_connection_name


def _get_database_url() -> str:
    from app.settings import Settings
    import os

    settings = Settings()
    
    # Use SQLite for development/testing if PostgreSQL is not available
    if settings.environment == "development" and settings.ai_bot_db_host == "localhost":
        return "sqlite+aiosqlite:///./test.db"
    
    return f"postgresql+asyncpg://{settings.ai_bot_db_user}:{settings.ai_bot_db_password}@{settings.ai_bot_db_host}:5432/{settings.ai_bot_db_name}"


DATABASE_URL: str = _get_database_url()
logger.info(f"Connecting to database: {DATABASE_URL}")

engine: Any = create_async_engine(DATABASE_URL, echo=settings.environment == "development")
# 非同期セッションオブジェクトを作成
AsyncSessionLocal: Any = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
)

Base: Any = declarative_base()


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session
