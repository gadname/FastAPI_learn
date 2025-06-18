from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_hello():
    """Test the /api/v1/hello/ endpoint returns the expected greeting."""
    response = client.get("/api/v1/hello/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, FastAPI!"}
