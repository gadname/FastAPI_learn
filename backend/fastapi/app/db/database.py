from typing import Any, AsyncGenerator
from urllib.parse import quote_plus

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.settings import settings
from app.utils.logging import logger


def _get_database_url() -> str:
    password = quote_plus(settings.ai_bot_db_password)
    return (
        f"postgresql+asyncpg://{settings.ai_bot_db_user}:{password}"
        f"@{settings.ai_bot_db_host}:5432/{settings.ai_bot_db_name}"
    )


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
