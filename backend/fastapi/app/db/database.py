from typing import Any, AsyncGenerator, Generator # Added Generator
from sqlalchemy import create_engine # Added for sync engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker, Session # Added Session for sync type hint
from app.settings import settings
from urllib.parse import quote_plus

ai_bot_db_user: str = settings.ai_bot_db_user
ai_bot_db_password: str = quote_plus(settings.ai_bot_db_password)
ai_bot_db_name: str = settings.ai_bot_db_name
ai_bot_db_host: str = settings.ai_bot_db_host
ai_bot_cloud_sql_connection_name: str = settings.ai_bot_cloud_sql_connection_name


# --- Asynchronous Setup ---
def _get_async_database_url() -> str:
    # Renamed to be specific
    from app.settings import Settings
    current_settings = Settings() # avoid conflict with global settings variable
    return f"postgresql+asyncpg://{current_settings.ai_bot_db_user}:{current_settings.ai_bot_db_password}@{current_settings.ai_bot_db_host}:5432/{current_settings.ai_bot_db_name}"

ASYNC_DATABASE_URL: str = _get_async_database_url()
print(f"Connecting to async database: {ASYNC_DATABASE_URL}")

async_engine: Any = create_async_engine(ASYNC_DATABASE_URL, echo=True) # Renamed engine to async_engine
AsyncSessionLocal: Any = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
)

Base: Any = declarative_base() # Base can be shared

async def get_db() -> AsyncGenerator[AsyncSession, None]: # This is the existing async get_db
    async with AsyncSessionLocal() as session:
        yield session

# --- Synchronous Setup ---
def _get_sync_database_url() -> str:
    from app.settings import Settings
    current_settings = Settings() # avoid conflict with global settings variable
    # Ensure you have 'psycopg2-binary' or 'psycopg2' installed for this to work
    return f"postgresql+psycopg2://{current_settings.ai_bot_db_user}:{current_settings.ai_bot_db_password}@{current_settings.ai_bot_db_host}:5432/{current_settings.ai_bot_db_name}"

SYNC_DATABASE_URL: str = _get_sync_database_url()
print(f"Connecting to sync database: {SYNC_DATABASE_URL}")

# For synchronous operations (e.g. for the new ADV chat endpoints if they remain sync)
# connect_args might be needed depending on SSL requirements or other parameters,
# but for simplicity, we'll omit them unless an error occurs.
# For SQLite, it would be: connect_args={"check_same_thread": False}
engine_sync: Any = create_engine(SYNC_DATABASE_URL, echo=True)
SessionLocal_sync: Any = sessionmaker(autocommit=False, autoflush=False, bind=engine_sync)

def get_db_sync() -> Generator[Session, None, None]: # New synchronous get_db
    db = SessionLocal_sync()
    try:
        yield db
    finally:
        db.close()

# リソースを安全に確保するため (Comment from original file)
