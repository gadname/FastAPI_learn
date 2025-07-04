import asyncio
from typing import AsyncGenerator, Generator

import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.db.base_class import Base  # All models should be imported here or via their modules
from app.models.user import User # Ensure User model is imported so Base knows about it
from app.main import app
from app.db.database import get_db
from app.schemas.user import UserCreate
from app.cruds.crud_user import create_user as crud_create_user
from app.utils.security import create_access_token
from .utils.user import get_random_user_create_schema, random_lower_string

# Use an in-memory SQLite database for testing
TEST_DATABASE_URL = "sqlite+aiosqlite:///./test.db"

# Create a new SQLAlchemy engine for testing
test_engine = create_async_engine(TEST_DATABASE_URL, echo=True)

# Create a new sessionmaker for testing
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=test_engine, class_=AsyncSession
)


async def override_get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency override for get_db that uses the test database.
    """
    async with TestingSessionLocal() as session:
        yield session

# Apply the override for the whole test session
app.dependency_overrides[get_db] = override_get_db


@pytest_asyncio.fixture(scope="session")
def event_loop(request) -> Generator[asyncio.AbstractEventLoop, None, None]:
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session", autouse=True)
async def setup_database():
    """
    Create database tables before tests run, and drop them after.
    This runs once per session.
    """
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture(scope="function") # Changed to function scope for db session
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Yields a database session for a test.
    Rolls back transactions after the test.
    """
    async with TestingSessionLocal() as session:
        await session.begin_nested() # For potential rollbacks within tests
        yield session
        await session.rollback() # Ensure clean state after each test


@pytest_asyncio.fixture(scope="function")
async def client(db_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    """
    Fixture for an AsyncClient, ensuring the app context is managed.
    The db_session fixture ensures that the override_get_db uses the function-scoped session.
    """
    # Override get_db for this specific client if further isolation is needed,
    # but app.dependency_overrides should handle it globally for tests.
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest_asyncio.fixture(scope="function")
async def test_user(db_session: AsyncSession) -> User:
    """
    Fixture to create a new user in the database for testing.
    """
    user_create_data = get_random_user_create_schema()
    user = await crud_create_user(db=db_session, user=user_create_data)
    return user


@pytest_asyncio.fixture(scope="function")
async def authenticated_client(
    client: AsyncClient, test_user: User, db_session: AsyncSession
) -> AsyncClient:
    """
    Fixture for an AsyncClient that is authenticated as the test_user.
    """
    # Login the user to get a token
    login_data = {
        "username": test_user.username,
        "password": "password", # This assumes you know the password or set a default
                                # We need to ensure test_user fixture creates user with known password
                                # For now, let's assume the crud_create_user does not return the plain password
                                # So, we'll create a new user with known password for this fixture for simplicity
    }

    # Re-create a user for whom we know the password, or update test_user to store plain_password
    user_schema = UserCreate(username=random_lower_string(), password="testpassword123")
    actual_test_user = await crud_create_user(db=db_session, user=user_schema)


    access_token = create_access_token(data={"sub": actual_test_user.username})

    client.headers.update({"Authorization": f"Bearer {access_token}"})
    return client


@pytest_asyncio.fixture(scope="function")
async def created_user_with_password(db_session: AsyncSession) -> tuple[User, str]:
    """
    Fixture to create a user and return the user object and plain password.
    """
    password = random_lower_string(12)
    user_create_data = UserCreate(username=random_lower_string(), password=password)
    user = await crud_create_user(db=db_session, user=user_create_data)
    return user, password
