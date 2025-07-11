import pytest
from unittest.mock import MagicMock, AsyncMock
from pydantic import BaseModel
from typing import List, Optional
from app.services.base.base_service import LegacyServiceAdapter, BaseCRUDService


# Mock schemas for testing
class TestCreateSchema(BaseModel):
    name: str
    description: str


class TestResponseSchema(BaseModel):
    id: str
    name: str
    description: str
    
    class Config:
        from_attributes = True


class TestAllResponseSchema(BaseModel):
    items: List[TestResponseSchema]


class TestUpdateRequestSchema(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None


class TestUpdateResponseSchema(BaseModel):
    id: str
    name: str
    description: str
    
    class Config:
        from_attributes = True


class TestDeleteResponseSchema(BaseModel):
    id: str


# Mock model for testing
class MockModel:
    def __init__(self, **kwargs):
        self.id = kwargs.get('id', 'test-123')
        self.name = kwargs.get('name', 'Test Name')
        self.description = kwargs.get('description', 'Test Description')


# Mock service for testing
class MockService:
    @staticmethod
    async def test_method():
        return "test_result"
    
    @staticmethod
    def sync_method():
        return "sync_result"


class TestLegacyServiceAdapter:
    def test_adapter_creation(self):
        """Test that the legacy service adapter can be created"""
        adapter = LegacyServiceAdapter(MockService)
        assert adapter.service_class == MockService
    
    def test_adapter_attribute_access(self):
        """Test that the adapter properly delegates attribute access"""
        adapter = LegacyServiceAdapter(MockService)
        
        # Test accessing a method
        assert hasattr(adapter, 'test_method')
        assert callable(getattr(adapter, 'test_method'))
        
        # Test accessing a sync method
        assert hasattr(adapter, 'sync_method')
        assert callable(getattr(adapter, 'sync_method'))
    
    def test_adapter_method_calls(self):
        """Test that the adapter properly delegates method calls"""
        adapter = LegacyServiceAdapter(MockService)
        
        # Test sync method call
        result = adapter.sync_method()
        assert result == "sync_result"


class TestBaseCRUDService:
    def test_service_creation(self):
        """Test that the base CRUD service can be created"""
        service = BaseCRUDService(
            model=MockModel,
            response_schema=TestResponseSchema,
            all_response_schema=TestAllResponseSchema,
            update_response_schema=TestUpdateResponseSchema,
            delete_response_schema=TestDeleteResponseSchema,
            entity_name="test_item",
            entity_name_jp="テスト項目",
        )
        
        assert service.model == MockModel
        assert service.entity_name == "test_item"
        assert service.entity_name_jp == "テスト項目"
    
    def test_service_abstract_methods(self):
        """Test that the service implements abstract methods"""
        service = BaseCRUDService(
            model=MockModel,
            response_schema=TestResponseSchema,
            all_response_schema=TestAllResponseSchema,
            update_response_schema=TestUpdateResponseSchema,
            delete_response_schema=TestDeleteResponseSchema,
            entity_name="test_item",
            entity_name_jp="テスト項目",
        )
        
        assert service.get_model() == MockModel
        assert service.get_entity_name() == "test_item"
        assert service.get_entity_name_jp() == "テスト項目"
    
    @pytest.mark.asyncio
    async def test_create_entity(self):
        """Test create entity functionality"""
        service = BaseCRUDService(
            model=MockModel,
            response_schema=TestResponseSchema,
            all_response_schema=TestAllResponseSchema,
            update_response_schema=TestUpdateResponseSchema,
            delete_response_schema=TestDeleteResponseSchema,
            entity_name="test_item",
            entity_name_jp="テスト項目",
        )
        
        # Mock database session
        mock_db = AsyncMock()
        mock_entity = MockModel(id="test-123", name="Test", description="Test Desc")
        mock_db.commit = AsyncMock()
        mock_db.refresh = AsyncMock()
        
        # Mock the model constructor
        original_model = service.model
        service.model = lambda **kwargs: mock_entity
        
        create_data = TestCreateSchema(name="Test", description="Test Desc")
        
        result = await service.create_entity(mock_db, create_data)
        
        assert isinstance(result, TestResponseSchema)
        assert result.name == "Test"
        assert result.description == "Test Desc"
        
        # Verify database operations were called
        mock_db.commit.assert_called_once()
        mock_db.refresh.assert_called_once()
        
        # Restore original model
        service.model = original_model
    
    @pytest.mark.asyncio
    async def test_create_entity_error_handling(self):
        """Test create entity error handling"""
        service = BaseCRUDService(
            model=MockModel,
            response_schema=TestResponseSchema,
            all_response_schema=TestAllResponseSchema,
            update_response_schema=TestUpdateResponseSchema,
            delete_response_schema=TestDeleteResponseSchema,
            entity_name="test_item",
            entity_name_jp="テスト項目",
        )
        
        # Mock database session that raises an error
        mock_db = AsyncMock()
        mock_db.commit.side_effect = Exception("Database error")
        mock_db.rollback = AsyncMock()
        
        create_data = TestCreateSchema(name="Test", description="Test Desc")
        
        with pytest.raises(Exception) as exc_info:
            await service.create_entity(mock_db, create_data)
        
        assert str(exc_info.value) == "Database error"
        mock_db.rollback.assert_called_once()