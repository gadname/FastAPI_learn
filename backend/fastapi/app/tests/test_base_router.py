"""Tests for base router functionality."""

from typing import Any, Dict, Generic, List, TypeVar
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from fastapi import HTTPException
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.base.base_router import BaseRouter, BaseCRUDRouter
from app.services.base.base_service import BaseService


# Test schemas for generic testing
class TestCreateSchema:
    def __init__(self, name: str):
        self.name = name


class TestResponseSchema:
    def __init__(self, id: str, name: str):
        self.id = id
        self.name = name


class TestUpdateSchema:
    def __init__(self, name: str):
        self.name = name


class TestService(BaseService):
    """Test service for base router testing."""
    
    @staticmethod
    async def create_item(db: AsyncSession, item: TestCreateSchema) -> TestResponseSchema:
        return TestResponseSchema(id="test-id", name=item.name)
    
    @staticmethod
    async def get_all_items(db: AsyncSession) -> List[TestResponseSchema]:
        return [TestResponseSchema(id="test-id", name="test-name")]
    
    @staticmethod
    async def get_item_by_id(db: AsyncSession, item_id: str) -> TestResponseSchema:
        if item_id == "invalid":
            raise ValueError("Item not found")
        return TestResponseSchema(id=item_id, name="test-name")
    
    @staticmethod
    async def update_item(item_id: str, item: TestUpdateSchema, db: AsyncSession) -> TestResponseSchema:
        if item_id == "invalid":
            raise ValueError("Item not found")
        return TestResponseSchema(id=item_id, name=item.name)
    
    @staticmethod
    async def delete_item(item_id: str, db: AsyncSession) -> Dict[str, Any]:
        if item_id == "invalid":
            raise ValueError("Item not found")
        return {"message": f"Item {item_id} deleted successfully"}


class TestCRUDRouter(BaseCRUDRouter):
    """Test CRUD router for testing base functionality."""
    
    def __init__(self):
        super().__init__(
            prefix="/test",
            tags=["test"],
            service=TestService,
            create_schema=TestCreateSchema,
            response_schema=TestResponseSchema,
            update_schema=TestUpdateSchema,
            delete_response_schema=dict,
            resource_name="test item"
        )


class TestBaseRouter:
    """Test cases for BaseRouter class."""
    
    def test_base_router_initialization(self):
        """Test that BaseRouter initializes correctly."""
        router = BaseRouter(prefix="/test", tags=["test"])
        assert router.prefix == "/test"
        assert router.tags == ["test"]
    
    def test_base_router_error_handling(self):
        """Test error handling in BaseRouter."""
        router = BaseRouter(prefix="/test", tags=["test"])
        
        # Test ValueError handling
        with pytest.raises(HTTPException) as exc_info:
            router._handle_error(ValueError("Test error"), "test operation")
        assert exc_info.value.status_code == 404
        
        # Test general Exception handling
        with pytest.raises(HTTPException) as exc_info:
            router._handle_error(Exception("Test error"), "test operation")
        assert exc_info.value.status_code == 500


class TestBaseCRUDRouter:
    """Test cases for BaseCRUDRouter class."""
    
    def test_crud_router_initialization(self):
        """Test that BaseCRUDRouter initializes correctly."""
        router = TestCRUDRouter()
        assert router.prefix == "/test"
        assert router.tags == ["test"]
        assert router.service == TestService
    
    @pytest.mark.asyncio
    async def test_create_endpoint(self):
        """Test the create endpoint."""
        router = TestCRUDRouter()
        db_mock = AsyncMock(spec=AsyncSession)
        
        # Test successful creation
        result = await router._create_item(TestCreateSchema("test"), db_mock)
        assert result.id == "test-id"
        assert result.name == "test"
    
    @pytest.mark.asyncio
    async def test_get_all_endpoint(self):
        """Test the get all endpoint."""
        router = TestCRUDRouter()
        db_mock = AsyncMock(spec=AsyncSession)
        
        # Test successful get all
        result = await router._get_all_items(db_mock)
        assert len(result) == 1
        assert result[0].id == "test-id"
    
    @pytest.mark.asyncio
    async def test_get_by_id_endpoint(self):
        """Test the get by ID endpoint."""
        router = TestCRUDRouter()
        db_mock = AsyncMock(spec=AsyncSession)
        
        # Test successful get by ID
        result = await router._get_item_by_id("test-id", db_mock)
        assert result.id == "test-id"
        
        # Test not found
        with pytest.raises(HTTPException) as exc_info:
            await router._get_item_by_id("invalid", db_mock)
        assert exc_info.value.status_code == 404
    
    @pytest.mark.asyncio
    async def test_update_endpoint(self):
        """Test the update endpoint."""
        router = TestCRUDRouter()
        db_mock = AsyncMock(spec=AsyncSession)
        
        # Test successful update
        result = await router._update_item("test-id", TestUpdateSchema("updated"), db_mock)
        assert result.id == "test-id"
        assert result.name == "updated"
        
        # Test not found
        with pytest.raises(HTTPException) as exc_info:
            await router._update_item("invalid", TestUpdateSchema("updated"), db_mock)
        assert exc_info.value.status_code == 404
    
    @pytest.mark.asyncio
    async def test_delete_endpoint(self):
        """Test the delete endpoint."""
        router = TestCRUDRouter()
        db_mock = AsyncMock(spec=AsyncSession)
        
        # Test successful delete
        result = await router._delete_item("test-id", db_mock)
        assert "message" in result
        
        # Test not found
        with pytest.raises(HTTPException) as exc_info:
            await router._delete_item("invalid", db_mock)
        assert exc_info.value.status_code == 404