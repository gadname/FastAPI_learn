import pytest
from httpx import AsyncClient
from fastapi import FastAPI
from unittest.mock import AsyncMock, patch

from app.main import app
# Import the dependency provider function
from app.api.v1.cat_image import get_cat_image_service
from app.services.cat_image import CatImageService
from app.schemas.cat_image import CatImageResponse

@pytest.mark.asyncio
async def test_get_cat_image_success():
    mock_service = AsyncMock(spec=CatImageService)
    mock_service.get_cat_image_url.return_value = "http://example.com/cat.jpg"

    # Override the dependency provider function
    app.dependency_overrides[get_cat_image_service] = lambda: mock_service

    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/api/v1/cat/image")

    assert response.status_code == 200
    json_response = response.json()
    assert json_response["url"] == "http://example.com/cat.jpg"
    CatImageResponse(**json_response)
    app.dependency_overrides = {}

@pytest.mark.asyncio
async def test_get_cat_image_service_error():
    mock_service = AsyncMock(spec=CatImageService)
    # Configure the mock to simulate an error that would lead to a 500 in the service
    # For example, if the service raises HTTPException(500, detail="...")
    # Here, we'll make it raise a generic Exception, which our endpoint's error handling
    # should catch and convert to an HTTPException.
    mock_service.get_cat_image_url.side_effect = Exception("Test service error")

    app.dependency_overrides[get_cat_image_service] = lambda: mock_service

    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/api/v1/cat/image")

    # The endpoint catches generic exceptions and re-raises as HTTPException(500, detail=f"An unexpected error occurred: {e}")
    assert response.status_code == 500
    # Check if the original error message is part of the detail
    # Based on the service, it re-raises with a generic message, let's adjust:
    # The service's generic exception is caught by the endpoint's service call,
    # which in turn is wrapped by CatImageService's own try-except that re-raises HTTPException.
    # The endpoint itself doesn't have a try-except, it relies on FastAPI's default exception handling
    # or specific exceptions raised by the service.
    # The CatImageService catches Exception and re-raises HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")
    assert "An unexpected error occurred: Test service error" in response.json()["detail"]
    app.dependency_overrides = {}
