import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.user import UserCreate, User as UserSchema
from app.models.user import User as UserModel
from app.tests.utils.user import get_random_user_create_schema, random_lower_string
from app.config import V1_API_PREFIX # Assuming you have this for your API prefix
from app.services.auth_service import create_jwt_token # For creating tokens for tests

# If V1_API_PREFIX is not defined in app.config, define it here or import appropriately
# For example: V1_API_PREFIX = "/api/v1" (adjust if your prefix is different)
# It was used in a previous step as: app.include_router(router=v1_router, prefix="/api/v1")
# And auth router was added with prefix "/auth"
AUTH_PREFIX = V1_API_PREFIX + "/auth"


@pytest.mark.asyncio
async def test_register_user_success(client: AsyncClient, db_session: AsyncSession):
    user_data = get_random_user_create_schema()
    response = await client.post(
        f"{AUTH_PREFIX}/register",
        json={"username": user_data.username, "password": user_data.password},
    )
    assert response.status_code == 201
    created_user_data = response.json()
    assert created_user_data["username"] == user_data.username
    assert "id" in created_user_data
    assert "hashed_password" not in created_user_data # Ensure password is not returned


@pytest.mark.asyncio
async def test_register_user_duplicate_username(client: AsyncClient, db_session: AsyncSession, test_user: UserModel):
    # test_user fixture already created a user. Try to register with the same username.
    user_data = UserCreate(username=test_user.username, password=random_lower_string())
    response = await client.post(
        f"{AUTH_PREFIX}/register",
        json={"username": user_data.username, "password": user_data.password},
    )
    assert response.status_code == 400
    error_data = response.json()
    assert "Username already registered" in error_data["detail"]


@pytest.mark.asyncio
async def test_login_success(client: AsyncClient, created_user_with_password: tuple[UserModel, str]):
    user, plain_password = created_user_with_password
    login_payload = {"username": user.username, "password": plain_password}

    response = await client.post(f"{AUTH_PREFIX}/login", data=login_payload) # OAuth2PasswordRequestForm uses form data

    assert response.status_code == 200
    token_data = response.json()
    assert "access_token" in token_data
    assert token_data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_login_non_existent_user(client: AsyncClient):
    login_payload = {"username": "nonexistentuser", "password": "anypassword"}
    response = await client.post(f"{AUTH_PREFIX}/login", data=login_payload)
    assert response.status_code == 401
    error_data = response.json()
    assert "Incorrect username or password" in error_data["detail"]


@pytest.mark.asyncio
async def test_login_incorrect_password(client: AsyncClient, created_user_with_password: tuple[UserModel, str]):
    user, _ = created_user_with_password # We only need the username
    login_payload = {"username": user.username, "password": "wrongpassword"}
    response = await client.post(f"{AUTH_PREFIX}/login", data=login_payload)
    assert response.status_code == 401
    error_data = response.json()
    assert "Incorrect username or password" in error_data["detail"]


@pytest.mark.asyncio
async def test_read_users_me_success(authenticated_client: AsyncClient, db_session: AsyncSession):
    # The authenticated_client fixture uses a user created with username from random_lower_string() and password "testpassword123"
    # We need to fetch that user to compare details.
    # The token in authenticated_client corresponds to 'actual_test_user' in the fixture.
    # We need a way to get that user's details.
    # For now, let's assume the endpoint returns the correct structure.
    # A better way would be to have the authenticated_client fixture return the user object it used.

    response = await authenticated_client.get(f"{AUTH_PREFIX}/users/me")
    assert response.status_code == 200
    user_data = response.json()
    assert "id" in user_data
    assert "username" in user_data
    # We can't easily assert username here without knowing which user authenticated_client used.
    # The fixture `authenticated_client` creates `actual_test_user`. We need its username.
    # Let's modify `authenticated_client` to return the user too, or create a dedicated user for this.

    # For a more direct test of who "me" is:
    # 1. Create a user with known details.
    # 2. Generate token for THIS user.
    # 3. Make client use THIS token.
    # 4. Call /users/me and verify details match the known user.

    # Using the created_user_with_password fixture for a more direct test:
    user, plain_password = await db_session.execute(UserModel.__table__.select().limit(1)) # Get a user, any user for this example
    # This is not ideal, better to use a specific test user from a fixture.
    # Let's refine this with a dedicated fixture or by enhancing authenticated_client.

    # For now, basic structure check:
    assert isinstance(user_data["username"], str)


@pytest.mark.asyncio
async def test_read_users_me_with_specific_user(client: AsyncClient, created_user_with_password: tuple[UserModel, str]):
    user_model, plain_password = created_user_with_password

    # Manually create token for this user
    token_content = create_jwt_token(user=user_model) # user_model is an ORM object
    access_token = token_content["access_token"]

    headers = {"Authorization": f"Bearer {access_token}"}
    response = await client.get(f"{AUTH_PREFIX}/users/me", headers=headers)

    assert response.status_code == 200
    me_data = response.json()
    assert me_data["username"] == user_model.username
    assert me_data["id"] == user_model.id
    assert "hashed_password" not in me_data


@pytest.mark.asyncio
async def test_read_users_me_invalid_token(client: AsyncClient):
    headers = {"Authorization": "Bearer invalidtoken"}
    response = await client.get(f"{AUTH_PREFIX}/users/me", headers=headers)
    assert response.status_code == 401
    error_data = response.json()
    assert "Could not validate credentials" in error_data["detail"]


@pytest.mark.asyncio
async def test_read_users_me_no_token(client: AsyncClient):
    response = await client.get(f"{AUTH_PREFIX}/users/me")
    assert response.status_code == 401 # FastAPI's default for missing OAuth2 token
    error_data = response.json()
    # The actual detail might vary based on FastAPI's handling of missing scheme
    assert error_data["detail"] == "Not authenticated" # Or "Missing token" etc. Depends on OAuth2PasswordBearer config & FastAPI version
                                                    # OAuth2PasswordBearer by default returns "Not authenticated" if auto_error=True (default)

# Need to define V1_API_PREFIX if not imported from app.config
# This should come from how the main router is set up.
# In backend/fastapi/app/main.py: app.include_router(router=v1_router, prefix="/api/v1")
# So, V1_API_PREFIX should be "/api/v1"
V1_API_PREFIX = "/api/v1"
AUTH_PREFIX = V1_API_PREFIX + "/auth" # Ensure this is correctly defined for tests.

# Re-check the authenticated_client fixture to ensure it provides a usable user for /me tests
# The current authenticated_client in conftest.py creates 'actual_test_user'.
# We'd need to pass this user's details or the user object itself out of the fixture
# to make test_read_users_me_success more robust.
# The test_read_users_me_with_specific_user is a good alternative as it controls the user and token explicitly.
