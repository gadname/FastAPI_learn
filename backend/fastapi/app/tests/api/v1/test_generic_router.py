import pytest
from fastapi import FastAPI, HTTPException, Depends
from fastapi.testclient import TestClient
from pydantic import BaseModel
from typing import List, Optional, Any, Dict
import uuid

# Import the generic_router_factory
# Assuming base_router.py is in backend/fastapi/app/api/v1/
from app.api.v1.base_router import generic_router_factory

# --- Mock Schemas ---
class MockCreateSchema(BaseModel):
    name: str
    value: Optional[int] = None

class MockUpdateSchema(BaseModel):
    name: Optional[str] = None
    value: Optional[int] = None

class MockResponseSchema(BaseModel):
    id: str
    name: str
    value: Optional[int] = None

    class Config:
        from_attributes = True # Pydantic v2, was orm_mode

class MockAllResponseSchema(BaseModel):
    items: List[MockResponseSchema]

class MockDeleteResponseSchema(BaseModel):
    id: str
    message: str

# --- Mock Service ---
class MockService:
    def __init__(self):
        self.items: Dict[str, MockResponseSchema] = {}
        self.force_error_on_next_call = False
        self.error_message = "Forced internal server error"

    async def create(self, db: Any, *, obj_in: MockCreateSchema) -> MockResponseSchema:
        if self.force_error_on_next_call:
            self.force_error_on_next_call = False
            raise Exception(self.error_message)
        item_id = str(uuid.uuid4())
        new_item = MockResponseSchema(id=item_id, name=obj_in.name, value=obj_in.value)
        self.items[item_id] = new_item
        return new_item

    async def get_multi(self, db: Any, *, skip: int = 0, limit: int = 100) -> MockAllResponseSchema:
        if self.force_error_on_next_call:
            self.force_error_on_next_call = False
            raise Exception(self.error_message)

        all_items = list(self.items.values())
        paginated_items = all_items[skip : skip + limit]
        return MockAllResponseSchema(items=paginated_items)

    async def get(self, db: Any, *, id: str) -> Optional[MockResponseSchema]:
        if self.force_error_on_next_call:
            self.force_error_on_next_call = False
            raise Exception(self.error_message)
        item = self.items.get(id)
        if not item:
            # Generic router expects ValueError for not found
            raise ValueError(f"Item with id {id} not found")
        return item

    async def update(self, db: Any, *, db_obj: MockResponseSchema, obj_in: MockUpdateSchema) -> MockResponseSchema:
        if self.force_error_on_next_call:
            self.force_error_on_next_call = False
            raise Exception(self.error_message)

        # db_obj is the existing item, fetched by generic_router.get()
        existing_item = self.items.get(db_obj.id)
        if not existing_item:
             # This case should ideally be caught by the get() call in the router first
            raise ValueError(f"Item with id {db_obj.id} not found for update")

        update_data = obj_in.model_dump(exclude_unset=True)
        if "name" in update_data:
            existing_item.name = update_data["name"]
        if "value" in update_data:
            existing_item.value = update_data["value"]

        self.items[existing_item.id] = existing_item
        return existing_item

    async def remove(self, db: Any, *, id: str) -> MockResponseSchema: # Changed to return MockResponseSchema as per current base_router
        if self.force_error_on_next_call:
            self.force_error_on_next_call = False
            raise Exception(self.error_message)

        item = self.items.pop(id, None)
        if not item:
            raise ValueError(f"Item with id {id} not found for deletion")
        # The generic router can be configured with a specific delete response model.
        # For this test, let's assume it returns the deleted item (MockResponseSchema)
        # or a MockDeleteResponseSchema if configured.
        # Current generic router's delete endpoint returns ModelType or DeleteModelType.
        # If DeleteModelType is not None, it's used. Else ModelType is used.
        # Here, we'll test with ModelType for delete response (i.e. MockResponseSchema)
        # And also with a specific DeleteModelType (MockDeleteResponseSchema) in another test setup.
        return item


# --- Test Setup (Fixture) ---
# Mock DB session dependency
async def mock_get_db():
    yield None # Or a mock session object if service methods require it

@pytest.fixture
def mock_service_instance():
    return MockService()

@pytest.fixture
def test_app_with_generic_router(mock_service_instance: MockService):
    app = FastAPI()

    # Override the get_db dependency for the app
    app.dependency_overrides[generic_router_factory.__globals__['get_db']] = mock_get_db

    test_router_instance = generic_router_factory(
        service=mock_service_instance,
        tags=["test_entity"],
        prefix="/test_entity",
        response_model=MockResponseSchema,
        create_schema=MockCreateSchema,
        update_schema=MockUpdateSchema,
        get_all_response_model=MockAllResponseSchema, # As per current generic_router
        # Not specifying update_response_model or delete_response_model initially
        # to test default behavior (uses response_model).
    )
    app.include_router(test_router_instance)
    return app

@pytest.fixture
def test_app_with_specific_delete_model(mock_service_instance: MockService):
    app = FastAPI()
    app.dependency_overrides[generic_router_factory.__globals__['get_db']] = mock_get_db

    # Special mock service method for custom delete response
    async def remove_custom_delete(db: Any, *, id: str) -> MockDeleteResponseSchema:
        if mock_service_instance.force_error_on_next_call:
            mock_service_instance.force_error_on_next_call = False
            raise Exception(mock_service_instance.error_message)
        item = mock_service_instance.items.pop(id, None)
        if not item:
            raise ValueError(f"Item with id {id} not found for deletion")
        return MockDeleteResponseSchema(id=id, message=f"Successfully deleted item {id}")

    # Temporarily patch the service instance for this test setup
    original_remove = mock_service_instance.remove
    mock_service_instance.remove = remove_custom_delete

    test_router_instance_custom_delete = generic_router_factory(
        service=mock_service_instance,
        tags=["test_entity_custom_delete"],
        prefix="/test_entity_custom_delete",
        response_model=MockResponseSchema,
        create_schema=MockCreateSchema,
        update_schema=MockUpdateSchema,
        get_all_response_model=MockAllResponseSchema,
        delete_response_model=MockDeleteResponseSchema # Specific delete model
    )
    app.include_router(test_router_instance_custom_delete)
    yield app # yield to allow cleanup

    # Restore original remove method
    mock_service_instance.remove = original_remove


# --- Test Cases ---
def test_create_item(test_app_with_generic_router: FastAPI, mock_service_instance: MockService):
    client = TestClient(test_app_with_generic_router)
    response = client.post("/test_entity/", json={"name": "Test Item", "value": 123})
    assert response.status_code == 201 # Default for POST success
    data = response.json()
    assert data["name"] == "Test Item"
    assert data["value"] == 123
    assert "id" in data
    assert data["id"] in mock_service_instance.items

def test_create_item_server_error(test_app_with_generic_router: FastAPI, mock_service_instance: MockService):
    client = TestClient(test_app_with_generic_router)
    mock_service_instance.force_error_on_next_call = True
    response = client.post("/test_entity/", json={"name": "Error Item"})
    assert response.status_code == 500
    assert response.json()["detail"] == "Internal server error"

def test_get_all_items(test_app_with_generic_router: FastAPI, mock_service_instance: MockService):
    client = TestClient(test_app_with_generic_router)
    # Pre-populate service
    item1_data = {"name": "Item 1"}
    item1 = asyncio.run(mock_service_instance.create(db=None, obj_in=MockCreateSchema(**item1_data)))

    response = client.get("/test_entity/")
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) >= 1 # Can be more if other tests populated
    assert any(item["id"] == item1.id for item in data["items"])

def test_get_all_items_server_error(test_app_with_generic_router: FastAPI, mock_service_instance: MockService):
    client = TestClient(test_app_with_generic_router)
    mock_service_instance.force_error_on_next_call = True
    response = client.get("/test_entity/")
    assert response.status_code == 500
    assert response.json()["detail"] == "Internal server error"

def test_get_one_item(test_app_with_generic_router: FastAPI, mock_service_instance: MockService):
    client = TestClient(test_app_with_generic_router)
    item_data = {"name": "Specific Item"}
    created_item = asyncio.run(mock_service_instance.create(db=None, obj_in=MockCreateSchema(**item_data)))

    response = client.get(f"/test_entity/{created_item.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == created_item.id
    assert data["name"] == "Specific Item"

def test_get_one_item_not_found(test_app_with_generic_router: FastAPI):
    client = TestClient(test_app_with_generic_router)
    non_existent_id = str(uuid.uuid4())
    response = client.get(f"/test_entity/{non_existent_id}")
    assert response.status_code == 404
    assert f"Item with id {non_existent_id} not found" in response.json()["detail"] # Based on ValueError in service

def test_get_one_item_server_error(test_app_with_generic_router: FastAPI, mock_service_instance: MockService):
    client = TestClient(test_app_with_generic_router)
    item_data = {"name": "Error Get Item"} # Item needs to exist for get to be called
    created_item = asyncio.run(mock_service_instance.create(db=None, obj_in=MockCreateSchema(**item_data)))

    mock_service_instance.force_error_on_next_call = True
    response = client.get(f"/test_entity/{created_item.id}")
    assert response.status_code == 500
    assert response.json()["detail"] == "Internal server error"

def test_update_item(test_app_with_generic_router: FastAPI, mock_service_instance: MockService):
    client = TestClient(test_app_with_generic_router)
    item_data = {"name": "Update Me", "value": 10}
    created_item = asyncio.run(mock_service_instance.create(db=None, obj_in=MockCreateSchema(**item_data)))

    update_payload = {"name": "Updated Name", "value": 20}
    response = client.put(f"/test_entity/{created_item.id}", json=update_payload)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == created_item.id
    assert data["name"] == "Updated Name"
    assert data["value"] == 20
    assert mock_service_instance.items[created_item.id].name == "Updated Name"

def test_update_item_not_found(test_app_with_generic_router: FastAPI):
    client = TestClient(test_app_with_generic_router)
    non_existent_id = str(uuid.uuid4())
    response = client.put(f"/test_entity/{non_existent_id}", json={"name": "Ghost Update"})
    assert response.status_code == 404
    # Detail message comes from the service's get() method before update() is called by router
    assert f"Item with id {non_existent_id} not found" in response.json()["detail"]

def test_update_item_server_error_on_get(test_app_with_generic_router: FastAPI, mock_service_instance: MockService):
    client = TestClient(test_app_with_generic_router)
    item_data = {"name": "Update Error Get"}
    created_item = asyncio.run(mock_service_instance.create(db=None, obj_in=MockCreateSchema(**item_data)))

    mock_service_instance.force_error_on_next_call = True # Error on the 'get' part of update
    response = client.put(f"/test_entity/{created_item.id}", json={"name": "Error Update"})
    assert response.status_code == 500
    # Error message from the .get() call within the router
    assert response.json()["detail"] == "Internal server error"


def test_update_item_server_error_on_update(test_app_with_generic_router: FastAPI, mock_service_instance: MockService):
    client = TestClient(test_app_with_generic_router)
    item_data = {"name": "Update Error Update"}
    created_item = asyncio.run(mock_service_instance.create(db=None, obj_in=MockCreateSchema(**item_data)))

    # Ensure 'get' succeeds, then 'update' fails
    mock_service_instance.force_error_on_next_call = False
    def force_error_on_update_only():
        mock_service_instance.force_error_on_next_call = True

    # This is a bit tricky; we want get() to succeed, then update() to fail.
    # The error flag will be set after get() is called by the router logic.
    # A more robust way would be to mock service.get() and service.update() separately via monkeypatching.
    # For now, let's assume the flag is flipped by another mechanism or by direct call if possible.
    # The current `force_error_on_next_call` is global to the service instance.
    # A simple way:
    original_update_method = mock_service_instance.update
    async def new_update(*args, **kwargs):
        raise Exception("Forced error during update operation")
    mock_service_instance.update = new_update

    response = client.put(f"/test_entity/{created_item.id}", json={"name": "Error Update"})
    assert response.status_code == 500
    assert response.json()["detail"] == "Internal server error"
    mock_service_instance.update = original_update_method # Restore


def test_delete_item(test_app_with_generic_router: FastAPI, mock_service_instance: MockService):
    client = TestClient(test_app_with_generic_router)
    item_data = {"name": "Delete Me"}
    created_item = asyncio.run(mock_service_instance.create(db=None, obj_in=MockCreateSchema(**item_data)))
    assert created_item.id in mock_service_instance.items

    response = client.delete(f"/test_entity/{created_item.id}")
    assert response.status_code == 200 # Default is ModelType (MockResponseSchema)
    data = response.json()
    assert data["id"] == created_item.id
    assert data["name"] == "Delete Me"
    assert created_item.id not in mock_service_instance.items

def test_delete_item_with_custom_response_model(test_app_with_specific_delete_model: FastAPI, mock_service_instance: MockService):
    client = TestClient(test_app_with_specific_delete_model)
    item_data = {"name": "Delete Me Custom"}
    # Need to use the service instance tied to this app to create item
    # The mock_service_instance is shared, which is fine.
    created_item = asyncio.run(mock_service_instance.create(db=None, obj_in=MockCreateSchema(**item_data)))
    assert created_item.id in mock_service_instance.items

    response = client.delete(f"/test_entity_custom_delete/{created_item.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == created_item.id
    assert data["message"] == f"Successfully deleted item {created_item.id}"
    assert created_item.id not in mock_service_instance.items


def test_delete_item_not_found(test_app_with_generic_router: FastAPI):
    client = TestClient(test_app_with_generic_router)
    non_existent_id = str(uuid.uuid4())
    response = client.delete(f"/test_entity/{non_existent_id}")
    assert response.status_code == 404
    assert f"Item with id {non_existent_id} not found" in response.json()["detail"]

def test_delete_item_server_error_on_get(test_app_with_generic_router: FastAPI, mock_service_instance: MockService):
    client = TestClient(test_app_with_generic_router)
    item_data = {"name": "Delete Error Get"}
    created_item = asyncio.run(mock_service_instance.create(db=None, obj_in=MockCreateSchema(**item_data)))

    mock_service_instance.force_error_on_next_call = True # Error on the 'get' part of delete
    response = client.delete(f"/test_entity/{created_item.id}")
    assert response.status_code == 500
    assert response.json()["detail"] == "Internal server error"

def test_delete_item_server_error_on_remove(test_app_with_generic_router: FastAPI, mock_service_instance: MockService):
    client = TestClient(test_app_with_generic_router)
    item_data = {"name": "Delete Error Remove"}
    created_item = asyncio.run(mock_service_instance.create(db=None, obj_in=MockCreateSchema(**item_data)))

    original_remove_method = mock_service_instance.remove
    async def new_remove(*args, **kwargs):
        raise Exception("Forced error during remove operation")
    mock_service_instance.remove = new_remove

    response = client.delete(f"/test_entity/{created_item.id}")
    assert response.status_code == 500
    assert response.json()["detail"] == "Internal server error"
    mock_service_instance.remove = original_remove_method # Restore

# Need asyncio for running async service methods directly in test setup if needed
import asyncio

# Note: The generic_router_factory uses `get_db` from its own global scope.
# `app.dependency_overrides[get_db]` might not work directly if `get_db` is imported like `from app.db.session import get_db`.
# Instead, we need to override it where it's defined or used.
# The current override `app.dependency_overrides[generic_router_factory.__globals__['get_db']] = mock_get_db`
# attempts to patch it in the module where generic_router_factory is defined. This is a common way.

# Further tests could include:
# - Testing with specific update_response_model.
# - Testing pagination parameters (skip, limit) for get_all_items if the mock service supported it more granularly.
# - Testing behavior when `obj_in` for update is partial. (Covered by Pydantic schema exclude_unset=True)

# A small correction: `from_attributes = True` for Pydantic v2, not `orm_mode = True`
# The `MockResponseSchema` already has this.
# The `asyncio.run()` calls in test setup for pre-populating data are fine for test simplicity.
# In a more complex scenario with event loops, one might use `asyncio.get_event_loop().run_until_complete()` or pytest-asyncio.
# For TestClient, it handles the event loop for HTTP calls.
# The current version of FastAPI's TestClient can run async functions directly.
# Example: `await mock_service_instance.create(...)` would need pytest-asyncio and async test functions.
# Using `asyncio.run()` is a simple way to execute these helper async calls if tests are not marked `async`.
# If tests were `async def test_...`, then `await` could be used directly.
# For simplicity with standard pytest, `asyncio.run` is acceptable here.

# One detail: `generic_router_factory.__globals__['get_db']` is a way to access get_db
# if it's in the same module as generic_router_factory. If get_db is imported into base_router.py,
# then it's `base_router_module.get_db` that needs to be patched, or use the above method if it works.
# The current override `app.dependency_overrides[generic_router_factory.__globals__['get_db']] = mock_get_db`
# should work if `get_db` is available in the global scope of the `base_router` module.
# This is usually true if it's imported as `from app.db.session import get_db`.

# Final check on MockService.remove:
# The generic router uses `response_model` for delete if `delete_response_model` is not set.
# So, by default, `MockService.remove` should return `MockResponseSchema`.
# The test `test_delete_item_with_custom_response_model` handles the case where `delete_response_model` is set.
# The `MockService.remove` is adapted in that fixture. My current `MockService.remove` returns `MockResponseSchema`, which is correct for default behavior.
# The `test_app_with_specific_delete_model` fixture correctly patches `mock_service_instance.remove` for that specific test case.
# This looks okay.
