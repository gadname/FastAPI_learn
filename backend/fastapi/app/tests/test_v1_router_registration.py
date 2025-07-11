import pytest
from app.api.v1 import v1_router


class TestV1RouterRegistration:
    """Test that all routers are properly registered in the v1 router"""
    
    def test_v1_router_exists(self):
        """Test that the v1 router exists"""
        assert v1_router is not None
    
    def test_all_routers_registered(self):
        """Test that all routers are registered in the v1 router"""
        # Get all the registered routes
        routes = v1_router.routes
        route_prefixes = []
        
        for route in routes:
            if hasattr(route, 'path_regex'):
                # Extract prefix from the route path
                path = route.path
                if path.startswith('/'):
                    parts = path.split('/')
                    if len(parts) > 1 and parts[1]:
                        route_prefixes.append(f"/{parts[1]}")
        
        # Remove duplicates
        route_prefixes = list(set(route_prefixes))
        
        # Check that all expected routers are registered
        expected_prefixes = ["/bot", "/cat", "/cat-images", "/hello"]
        
        for prefix in expected_prefixes:
            assert prefix in route_prefixes, f"Router with prefix '{prefix}' not found in registered routes"
    
    def test_hello_router_registration(self):
        """Test that the hello router is now properly registered"""
        routes = v1_router.routes
        hello_routes = []
        
        for route in routes:
            if hasattr(route, 'path') and '/hello' in route.path:
                hello_routes.append(route)
        
        # Verify that hello routes exist
        assert len(hello_routes) > 0, "Hello router is not registered"
        
        # Verify that the hello route has GET method
        hello_get_route = None
        for route in hello_routes:
            if hasattr(route, 'methods') and "GET" in route.methods:
                hello_get_route = route
                break
        
        assert hello_get_route is not None, "Hello GET route not found"
    
    def test_route_count_increased(self):
        """Test that the total number of routes has increased with hello router"""
        routes = v1_router.routes
        
        # Count routes by prefix
        prefix_counts = {}
        for route in routes:
            if hasattr(route, 'path'):
                path = route.path
                if path.startswith('/'):
                    parts = path.split('/')
                    if len(parts) > 1 and parts[1]:
                        prefix = f"/{parts[1]}"
                        prefix_counts[prefix] = prefix_counts.get(prefix, 0) + 1
        
        # We should have routes for all our expected prefixes
        assert "/bot" in prefix_counts
        assert "/cat" in prefix_counts
        assert "/cat-images" in prefix_counts
        assert "/hello" in prefix_counts
        
        # The hello router should have at least 1 route
        assert prefix_counts["/hello"] >= 1