import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from app.cruds.crud_user import create_user, get_user_by_username
from app.schemas.user import UserCreate
from app.utils.security import verify_password
from app.tests.utils.user import random_lower_string


@pytest.mark.asyncio
async def test_create_user(db_session: AsyncSession):
    username = random_lower_string()
    password = "testpassword123"
    user_in = UserCreate(username=username, password=password)

    created_user = await create_user(db=db_session, user=user_in)

    assert created_user is not None
    assert created_user.username == username
    assert hasattr(created_user, "hashed_password")
    assert created_user.hashed_password is not None
    assert verify_password(password, created_user.hashed_password)


@pytest.mark.asyncio
async def test_get_user_by_username_existing(db_session: AsyncSession):
    username = random_lower_string()
    password = "testpasswordsecure"
    user_in = UserCreate(username=username, password=password)
    await create_user(db=db_session, user=user_in) # Create the user first

    retrieved_user = await get_user_by_username(db=db_session, username=username)

    assert retrieved_user is not None
    assert retrieved_user.username == username


@pytest.mark.asyncio
async def test_get_user_by_username_non_existing(db_session: AsyncSession):
    username = random_lower_string() # A username that doesn't exist
    retrieved_user = await get_user_by_username(db=db_session, username=username)
    assert retrieved_user is None


@pytest.mark.asyncio
async def test_create_user_duplicate_username(db_session: AsyncSession):
    username = random_lower_string()
    password = "testpassword1"
    user_in_1 = UserCreate(username=username, password=password)
    await create_user(db=db_session, user=user_in_1)

    password_2 = "testpassword2"
    user_in_2 = UserCreate(username=username, password=password_2)

    # Depending on DB constraints, this might raise an IntegrityError
    # The CRUD function itself doesn't check for duplicates before attempting insertion.
    # This check is typically done at the service layer or by DB constraints.
    # For now, let's assume the DB will raise an error.
    # If not, the test should reflect the actual behavior of crud_user.create_user.
    from sqlalchemy.exc import IntegrityError
    with pytest.raises(IntegrityError): # Or the specific exception your DB driver raises
        await create_user(db=db_session, user=user_in_2)
        # Note: If the previous create_user committed, this session might be dirty.
        # The rollback in db_session fixture should handle this.
        # However, it's good practice for create_user to handle this or for services to check first.
        # The current `create_user` does `db.add()` then `db.commit()`.
        # So the second call will indeed try to commit again.
        # If the test DB (SQLite) enforces uniqueness, this will fail as expected.

# To make this test more robust for crud_user, it might be better to check
# if the user was actually created or not if no exception is expected at CRUD level.
# However, testing for IntegrityError is a valid test for database interaction.
