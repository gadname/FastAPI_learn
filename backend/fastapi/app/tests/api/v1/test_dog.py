import pytest
from fastapi.testclient import TestClient
from app.main import app  # Import the main FastAPI app
from app.services.dog_service import db_dogs # Import for direct manipulation/cleanup

# Fixture to clean up the in-memory database before each test
@pytest.fixture(autouse=True)
def clear_db_dogs():
    db_dogs.clear()

client = TestClient(app)

def test_create_dog():
    response = client.post("/api/v1/dogs/", json={"name": "Buddy", "breed": "Golden Retriever", "age": 3})
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Buddy"
    assert data["breed"] == "Golden Retriever"
    assert data["age"] == 3
    assert "id" in data
    # Check if it's in our in-memory db
    assert data["id"] in db_dogs

def test_get_all_dogs_empty():
    response = client.get("/api/v1/dogs/")
    assert response.status_code == 200
    data = response.json()
    assert data["dogs"] == []
    assert data["count"] == 0

def test_get_all_dogs_with_data():
    # Create a dog first
    dog_data = {"name": "Lucy", "breed": "Beagle", "age": 5}
    create_response = client.post("/api/v1/dogs/", json=dog_data)
    created_dog_id = create_response.json()["id"]

    response = client.get("/api/v1/dogs/")
    assert response.status_code == 200
    data = response.json()
    assert len(data["dogs"]) == 1
    assert data["count"] == 1
    assert data["dogs"][0]["name"] == "Lucy"
    assert data["dogs"][0]["id"] == created_dog_id

def test_get_dog_by_id_found():
    dog_data = {"name": "Charlie", "breed": "Poodle", "age": 2}
    create_response = client.post("/api/v1/dogs/", json=dog_data)
    dog_id = create_response.json()["id"]

    response = client.get(f"/api/v1/dogs/{dog_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Charlie"
    assert data["breed"] == "Poodle"
    assert data["age"] == 2
    assert data["id"] == dog_id

def test_get_dog_by_id_not_found():
    response = client.get("/api/v1/dogs/non_existent_id")
    assert response.status_code == 404
    assert response.json()["detail"] == "Dog not found"

def test_update_dog_found():
    dog_data = {"name": "Max", "breed": "Labrador", "age": 4}
    create_response = client.post("/api/v1/dogs/", json=dog_data)
    dog_id = create_response.json()["id"]

    update_data = {"name": "Maximus", "age": 5}
    response = client.put(f"/api/v1/dogs/{dog_id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Maximus"
    assert data["age"] == 5
    assert data["breed"] == "Labrador" # Breed should remain unchanged
    assert data["id"] == dog_id
    # Check in-memory db
    assert db_dogs[dog_id]["name"] == "Maximus"

def test_update_dog_not_found():
    response = client.put("/api/v1/dogs/non_existent_id", json={"name": "Ghost"})
    assert response.status_code == 404
    assert response.json()["detail"] == "Dog not found for update"


def test_delete_dog_found():
    dog_data = {"name": "Bella", "breed": "Chihuahua", "age": 1}
    create_response = client.post("/api/v1/dogs/", json=dog_data)
    dog_id = create_response.json()["id"]
    assert dog_id in db_dogs # Ensure it's there before delete

    response = client.delete(f"/api/v1/dogs/{dog_id}")
    assert response.status_code == 200
    assert response.json() == {"message": "Dog deleted successfully"}
    assert dog_id not in db_dogs # Ensure it's gone

def test_delete_dog_not_found():
    response = client.delete("/api/v1/dogs/non_existent_id")
    assert response.status_code == 404
    assert response.json()["detail"] == "Dog not found for deletion"
