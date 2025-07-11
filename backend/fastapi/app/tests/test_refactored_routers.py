import pytest
from unittest.mock import patch, AsyncMock
from app.api.v1.bot import router as bot_router
from app.api.v1.cat import router as cat_router
from app.api.v1.hello import router as hello_router


class TestRefactoredRouters:
    """Test the refactored routers to ensure they work correctly"""
    
    def test_bot_router_exists(self):
        """Test that the bot router exists and has the correct configuration"""
        assert bot_router is not None
        assert bot_router.prefix == "/bot"
        assert "bot" in bot_router.tags
    
    def test_cat_router_exists(self):
        """Test that the cat router exists and has the correct configuration"""
        assert cat_router is not None
        assert cat_router.prefix == "/cat"
        assert "cat" in cat_router.tags
    
    def test_hello_router_exists(self):
        """Test that the hello router exists and has the correct configuration"""
        assert hello_router is not None
        assert hello_router.prefix == "/hello"
        assert "hello" in hello_router.tags
    
    def test_bot_router_routes(self):
        """Test that the bot router has all CRUD routes"""
        routes = bot_router.routes
        route_paths = [route.path for route in routes]
        
        # Check that all expected routes exist
        assert "/bot/" in route_paths
        assert "/bot/{entity_id}" in route_paths
        
        # Check HTTP methods
        route_methods = []
        for route in routes:
            if hasattr(route, 'methods'):
                route_methods.extend(route.methods)
        
        assert "POST" in route_methods
        assert "GET" in route_methods
        assert "PUT" in route_methods
        assert "DELETE" in route_methods
    
    def test_cat_router_routes(self):
        """Test that the cat router has all CRUD routes"""
        routes = cat_router.routes
        route_paths = [route.path for route in routes]
        
        # Check that all expected routes exist
        assert "/cat/" in route_paths
        assert "/cat/{entity_id}" in route_paths
        
        # Check HTTP methods
        route_methods = []
        for route in routes:
            if hasattr(route, 'methods'):
                route_methods.extend(route.methods)
        
        assert "POST" in route_methods
        assert "GET" in route_methods
        assert "PUT" in route_methods
        assert "DELETE" in route_methods
    
    def test_hello_router_routes(self):
        """Test that the hello router has the correct routes"""
        routes = hello_router.routes
        route_paths = [route.path for route in routes]
        
        # Check that the hello route exists
        assert "/hello/" in route_paths
        
        # Check HTTP methods
        route_methods = []
        for route in routes:
            if hasattr(route, 'methods'):
                route_methods.extend(route.methods)
        
        assert "GET" in route_methods
    
    def test_router_code_reduction(self):
        """Test that the routers have been significantly reduced in size"""
        # This test verifies that the refactored routers are much smaller
        # than the original implementation
        
        # Original bot.py had 79 lines, refactored should be around 29 lines
        # This is a rough estimate based on line count reduction
        
        # We can't directly measure lines in the test, but we can verify
        # that the routers are using the base classes
        from app.api.v1.bot import bot_router as bot_router_instance
        from app.api.v1.cat import cat_router as cat_router_instance
        
        # Verify that they're using the base CRUD router structure
        assert hasattr(bot_router_instance, 'service_class')
        assert hasattr(bot_router_instance, 'entity_name')
        assert hasattr(bot_router_instance, 'entity_name_jp')
        
        assert hasattr(cat_router_instance, 'service_class')
        assert hasattr(cat_router_instance, 'entity_name')
        assert hasattr(cat_router_instance, 'entity_name_jp')
        
        # Verify entity names are correct
        assert bot_router_instance.entity_name == "chat_bot"
        assert bot_router_instance.entity_name_jp == "ボット"
        
        assert cat_router_instance.entity_name == "cat"
        assert cat_router_instance.entity_name_jp == "猫"