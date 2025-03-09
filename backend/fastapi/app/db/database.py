from typing import Any, AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker
from app.settings import settings
from urllib.parse import quote_plus

ai_bot_db_user: str = settings.ai_bot_db_user
ai_bot_db_password: str = quote_plus(settings.ai_bot_db_password)
ai_bot_db_name: str = settings.ai_bot_db_name
ai_bot_db_host: str = settings.ai_bot_db_host
ai_bot_cloud_sql_connection_name: str = settings.ai_bot_cloud_sql_connection_name


def _get_database_url() -> str:
    base_url: str = f"postgresql+asyncpg://{ai_bot_db_user}:{ai_bot_db_password}@"
    if settings.environment == "production":
        return f"{base_url}/{ai_bot_db_name}?unix_socket=/cloudsql/{ai_bot_cloud_sql_connection_name}"
    else:
        return f"{base_url}{ai_bot_db_host}:5432/{ai_bot_db_name}"


DATABASE_URL: str = _get_database_url()
print(f"Connecting to database: {DATABASE_URL}")

engine: Any = create_async_engine(DATABASE_URL, echo=True)
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


# リソースを安全に確保するため
