import pytest
from fastapi.testclient import TestClient
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional
from app.api.base.base_router import BaseCRUDRouter
from app.services.base.base_service import LegacyServiceAdapter


# Mock schemas for testing
class TestCreateSchema(BaseModel):
    name: str
    description: str


class TestResponseSchema(BaseModel):
    id: str
    name: str
    description: str


class TestAllResponseSchema(BaseModel):
    items: List[TestResponseSchema]


class TestUpdateRequestSchema(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None


class TestUpdateResponseSchema(BaseModel):
    id: str
    name: str
    description: str


class TestDeleteResponseSchema(BaseModel):
    id: str


# Mock service for testing
class MockTestService:
    @staticmethod
    async def create_test_item(db, item):
        return TestResponseSchema(
            id="test-123",
            name=item.name,
            description=item.description
        )
    
    @staticmethod
    async def get_all_test_items(db):
        return TestAllResponseSchema(
            items=[
                TestResponseSchema(
                    id="test-1",
                    name="Test Item 1",
                    description="Description 1"
                ),
                TestResponseSchema(
                    id="test-2",
                    name="Test Item 2",
                    description="Description 2"
                )
            ]
        )
    
    @staticmethod
    async def get_test_item_by_id(db, item_id):
        if item_id == "404":
            raise ValueError("Item not found")
        return TestResponseSchema(
            id=item_id,
            name="Test Item",
            description="Test Description"
        )
    
    @staticmethod
    async def update_test_item(item_id, request, db):
        if item_id == "404":
            raise ValueError("Item not found")
        return TestUpdateResponseSchema(
            id=item_id,
            name=request.name or "Updated Name",
            description=request.description or "Updated Description"
        )
    
    @staticmethod
    async def delete_test_item(item_id, db):
        if item_id == "404":
            raise ValueError("Item not found")
        return TestDeleteResponseSchema(id=item_id)


class TestBaseCRUDRouter:
    def test_router_creation(self):
        """Test that the base CRUD router can be created successfully"""
        test_router = BaseCRUDRouter(
            prefix="/test",
            tags=["test"],
            service_class=LegacyServiceAdapter(MockTestService),
            create_schema=TestCreateSchema,
            response_schema=TestResponseSchema,
            all_response_schema=TestAllResponseSchema,
            update_request_schema=TestUpdateRequestSchema,
            update_response_schema=TestUpdateResponseSchema,
            delete_response_schema=TestDeleteResponseSchema,
            entity_name="test_item",
            entity_name_jp="テスト項目",
        )
        
        assert test_router.router is not None
        assert test_router.router.prefix == "/test"
        assert test_router.router.tags == ["test"]
    
    def test_router_routes_exist(self):
        """Test that all CRUD routes are properly created"""
        test_router = BaseCRUDRouter(
            prefix="/test",
            tags=["test"],
            service_class=LegacyServiceAdapter(MockTestService),
            create_schema=TestCreateSchema,
            response_schema=TestResponseSchema,
            all_response_schema=TestAllResponseSchema,
            update_request_schema=TestUpdateRequestSchema,
            update_response_schema=TestUpdateResponseSchema,
            delete_response_schema=TestDeleteResponseSchema,
            entity_name="test_item",
            entity_name_jp="テスト項目",
        )
        
        routes = test_router.router.routes
        route_paths = [route.path for route in routes]
        
        # Check that all expected routes exist
        assert "/test/" in route_paths
        assert "/test/{entity_id}" in route_paths
        
        # Check HTTP methods
        route_methods = []
        for route in routes:
            if hasattr(route, 'methods'):
                route_methods.extend(route.methods)
        
        assert "POST" in route_methods
        assert "GET" in route_methods
        assert "PUT" in route_methods
        assert "DELETE" in route_methods