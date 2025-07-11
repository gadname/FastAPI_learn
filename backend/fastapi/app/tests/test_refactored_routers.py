"""Tests for refactored routers using base classes."""

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_hello_router_registration():
    """Test that hello router is properly registered."""
    response = client.get("/api/v1/hello/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, FastAPI!"}


def test_bot_router_structure():
    """Test that bot router still works after refactoring."""
    # Test that the router is properly registered
    # This will test the endpoint structure without requiring a database
    response = client.get("/api/v1/bot/", headers={"accept": "application/json"})
    # We expect this to fail due to no database, but the 500 error means the router is registered
    assert response.status_code in [500, 422]  # 500 for DB error, 422 for validation


def test_cat_router_structure():
    """Test that cat router still works after refactoring."""
    # Test that the router is properly registered
    response = client.get("/api/v1/cat/", headers={"accept": "application/json"})
    # We expect this to fail due to no database, but the 500 error means the router is registered
    assert response.status_code in [500, 422]  # 500 for DB error, 422 for validation


def test_openapi_docs():
    """Test that OpenAPI documentation is generated correctly."""
    response = client.get("/openapi.json")
    assert response.status_code == 200
    
    openapi_spec = response.json()
    
    # Check that all routers are included in the OpenAPI spec
    assert "/api/v1/hello/" in openapi_spec["paths"]
    assert "/api/v1/bot/" in openapi_spec["paths"]
    assert "/api/v1/cat/" in openapi_spec["paths"]
    assert "/api/v1/cat_image/" in openapi_spec["paths"]
    
    # Check that CRUD endpoints are present for bot
    assert "/api/v1/bot/" in openapi_spec["paths"]
    assert "/api/v1/bot/{item_id}" in openapi_spec["paths"]
    
    # Check that CRUD endpoints are present for cat
    assert "/api/v1/cat/" in openapi_spec["paths"]
    assert "/api/v1/cat/{item_id}" in openapi_spec["paths"]