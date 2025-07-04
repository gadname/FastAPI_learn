import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import IntegrityError

from app.main import app
from app.db.database import Base, get_db
from app.models.user import User as UserModel
from app.schemas.user import UserCreate
from app.cruds.user import create_user as crud_create_user, get_user_by_username

# Use a separate SQLite in-memory database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create tables at the beginning of the test session
Base.metadata.create_all(bind=engine)

# Dependency override for test DB session
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

# Fixture to create a clean database for each test function
@pytest.fixture(scope="function", autouse=True)
def clean_db():
    Base.metadata.drop_all(bind=engine) # Drop all tables
    Base.metadata.create_all(bind=engine) # Recreate them
    yield
    # No explicit teardown needed here for in-memory,
    # but if using a persistent test DB, you might clean up users


TEST_USER_USERNAME = "testuser@example.com"
TEST_USER_PASSWORD = "testpassword"

def create_test_user_directly(db: Session, username: str = TEST_USER_USERNAME, password: str = TEST_USER_PASSWORD) -> UserModel:
    user_in = UserCreate(username=username, password=password)
    # Check if user already exists
    db_user = get_user_by_username(db, username=username)
    if db_user:
        return db_user
    try:
        return crud_create_user(db=db, user=user_in)
    except IntegrityError: # Should not happen if get_user_by_username check is done
        db.rollback()
        return get_user_by_username(db, username=username)


def test_register_user():
    # Test successful registration
    response = client.post(
        "/api/v1/auth/users/",
        json={"username": "newuser@example.com", "password": "newpassword"},
    )
    assert response.status_code == 200 # Assuming 200 for user creation based on auth.py
    data = response.json()
    assert data["username"] == "newuser@example.com"
    assert "id" in data
    assert "hashed_password" not in data # Ensure password is not returned

    # Verify user in DB (optional, but good practice)
    db = TestingSessionLocal()
    user_in_db = get_user_by_username(db, username="newuser@example.com")
    assert user_in_db is not None
    assert user_in_db.username == "newuser@example.com"
    db.close()

    # Test duplicate username registration
    response = client.post(
        "/api/v1/auth/users/",
        json={"username": "newuser@example.com", "password": "anotherpassword"},
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Username already registered"


def test_login_for_access_token():
    # Create a user first using the client (or directly in DB for isolated testing)
    client.post(
        "/api/v1/auth/users/",
        json={"username": TEST_USER_USERNAME, "password": TEST_USER_PASSWORD},
    )

    # Test successful login
    login_data = {"username": TEST_USER_USERNAME, "password": TEST_USER_PASSWORD}
    response = client.post("/api/v1/auth/token", data=login_data)
    assert response.status_code == 200
    token_data = response.json()
    assert "access_token" in token_data
    assert token_data["token_type"] == "bearer"

    # Test login with incorrect password
    login_data_wrong_pass = {"username": TEST_USER_USERNAME, "password": "wrongpassword"}
    response = client.post("/api/v1/auth/token", data=login_data_wrong_pass)
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect username or password"
    assert "WWW-Authenticate" in response.headers # Check for Bearer challenge

    # Test login with non-existent user
    login_data_non_existent_user = {"username": "nosuchuser@example.com", "password": "anypassword"}
    response = client.post("/api/v1/auth/token", data=login_data_non_existent_user)
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect username or password"

# For this test, we need a secured endpoint. Let's assume /api/v1/cat/ (the GET all cats endpoint) is secured.
# If cat.py uses AsyncSession, this test might fail or behave unexpectedly due to sync TestClient
# and the get_db override providing a sync session.
# This highlights the async/sync challenge.
def test_access_secured_endpoint_with_token():
    # 1. Register and Login to get a token
    client.post(
        "/api/v1/auth/users/",
        json={"username": "secureuser@example.com", "password": "securepassword"},
    )
    login_resp = client.post(
        "/api/v1/auth/token",
        data={"username": "secureuser@example.com", "password": "securepassword"},
    )
    token = login_resp.json()["access_token"]

    # 2. Access secured endpoint with token
    headers = {"Authorization": f"Bearer {token}"}
    # Assuming /api/v1/cat/ is the secured endpoint (from previous subtask)
    # Note: The actual path for "get_all_cats" in cat.py is /api/v1/cat/ (prefix="/cat", path="/")
    response_secured = client.get("/api/v1/cat/", headers=headers)
    # If this endpoint expects an AsyncSession and gets a sync one via override, it might error out.
    # If it works, it means FastAPI/Starlette might handle this transition, or the endpoint doesn't hit DB in a way that fails.
    assert response_secured.status_code == 200
    # Add more assertions based on the expected response of /api/v1/cat/ if needed.
    # For example, if it returns a list: assert isinstance(response_secured.json().get("cats"), list)


    # 3. Test without token
    response_no_token = client.get("/api/v1/cat/")
    assert response_no_token.status_code == 401 # Expecting 401 Unauthorized

    # 4. Test with invalid token
    headers_invalid = {"Authorization": "Bearer bogus"}
    response_invalid_token = client.get("/api/v1/cat/", headers=headers_invalid)
    assert response_invalid_token.status_code == 401 # Expecting 401 Unauthorized
    assert response_invalid_token.json().get("detail") == "Could not validate credentials"

# Placeholder for a test that might require an admin user, if roles were implemented
# def test_get_current_active_admin_user():
#     pass

# It's good practice to also test what happens if a user is marked inactive,
# but that requires functionality to update user's is_active status first.
# def test_access_with_inactive_user():
#    # 1. Create user
#    # 2. Log in, get token
#    # 3. Mark user as inactive in DB (requires a CRUD op for user update)
#    # 4. Try to access secured endpoint -> should fail (400 Bad Request "Inactive user")
#    pass

# Clean up the app.dependency_overrides after tests if needed, though for TestClient it's usually fine
# def fin():
# app.dependency_overrides = {}
# request.addfinalizer(fin)
# pytest.addfinalizer(fin) # This is not standard pytest usage for finalizers.
# Typically, fixtures handle setup/teardown. The current `clean_db` fixture handles DB state.
# Overrides persist for the TestClient's app instance.
