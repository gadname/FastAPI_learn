import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch
from app.main import app
from app.api.v1.cat_image import get_cat_image_service
from app.services.cat_image import CatImageService

client = TestClient(app)


def test_get_cat_image_success():
    """Test the /api/v1/cat-images/ endpoint returns a cat image URL successfully."""
    mock_service = AsyncMock(spec=CatImageService)
    mock_service.get_cat_image_url.return_value = "http://example.com/cat.jpg"

    app.dependency_overrides[get_cat_image_service] = lambda: mock_service

    response = client.get("/api/v1/cat-images/")

    assert response.status_code == 200
    json_response = response.json()
    assert json_response["url"] == "http://example.com/cat.jpg"

    # Clean up
    app.dependency_overrides = {}


def test_get_cat_image_service_error():
    """Test the /api/v1/cat-images/ endpoint handles service errors properly."""
    mock_service = AsyncMock(spec=CatImageService)
    mock_service.get_cat_image_url.side_effect = Exception("Test service error")

    app.dependency_overrides[get_cat_image_service] = lambda: mock_service

    response = client.get("/api/v1/cat-images/")

    assert response.status_code == 500
    assert (
        "An unexpected error occurred while fetching cat image"
        in response.json()["detail"]
    )

    # Clean up
    app.dependency_overrides = {}
