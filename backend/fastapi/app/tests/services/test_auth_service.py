import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

from app.services.auth_service import (
    register_new_user,
    authenticate_user,
    create_jwt_token,
)
from app.schemas.user import UserCreate
from app.models.user import User as UserModel # Import the SQLAlchemy model
from app.tests.utils.user import get_random_user_create_schema, random_lower_string


@pytest.mark.asyncio
async def test_register_new_user_success(db_session: AsyncSession):
    user_in = get_random_user_create_schema()
    user = await register_new_user(db=db_session, user_create=user_in)
    assert user is not None
    assert user.username == user_in.username
    assert hasattr(user, "hashed_password")


@pytest.mark.asyncio
async def test_register_new_user_duplicate_username(db_session: AsyncSession):
    user_in = get_random_user_create_schema()
    await register_new_user(db=db_session, user_create=user_in) # First registration

    with pytest.raises(HTTPException) as excinfo:
        await register_new_user(db=db_session, user_create=user_in) # Try to register again
    assert excinfo.value.status_code == 400
    assert "Username already registered" in excinfo.value.detail


@pytest.mark.asyncio
async def test_authenticate_user_success(db_session: AsyncSession):
    password = "strongpassword123"
    user_in_create = UserCreate(username=random_lower_string(), password=password)
    await register_new_user(db=db_session, user_create=user_in_create)

    authenticated_user = await authenticate_user(
        db=db_session, username=user_in_create.username, password=password
    )
    assert authenticated_user is not None
    assert authenticated_user.username == user_in_create.username


@pytest.mark.asyncio
async def test_authenticate_user_wrong_password(db_session: AsyncSession):
    password = "strongpassword123"
    user_in_create = UserCreate(username=random_lower_string(), password=password)
    await register_new_user(db=db_session, user_create=user_in_create)

    authenticated_user = await authenticate_user(
        db=db_session, username=user_in_create.username, password="wrongpassword"
    )
    assert authenticated_user is None


@pytest.mark.asyncio
async def test_authenticate_user_non_existent_username(db_session: AsyncSession):
    authenticated_user = await authenticate_user(
        db=db_session, username="nonexistentuser", password="anypassword"
    )
    assert authenticated_user is None


@pytest.mark.asyncio
async def test_create_jwt_token(db_session: AsyncSession):
    # First, create a user to pass to the function
    password = "jwtpassword"
    user_data = UserCreate(username=random_lower_string(), password=password)
    # We need a UserModel instance, so we register and then fetch, or construct one if appropriate
    # For this service function, it expects a UserModel.
    # Let's register and then fetch the user model instance.
    registered_user_from_service = await register_new_user(db=db_session, user_create=user_data)

    # Ensure we have a valid UserModel instance
    assert isinstance(registered_user_from_service, UserModel)

    token_data = create_jwt_token(user=registered_user_from_service)
    assert "access_token" in token_data
    assert "token_type" in token_data
    assert token_data["token_type"] == "bearer"
    assert isinstance(token_data["access_token"], str)

    # Optionally, decode to verify content if needed, though security utils test this more thoroughly
    from app.utils.security import decode_access_token
    decoded = decode_access_token(token_data["access_token"])
    assert decoded.username == registered_user_from_service.username
