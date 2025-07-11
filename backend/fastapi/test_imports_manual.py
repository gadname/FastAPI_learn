#!/usr/bin/env python3
"""Manual import tests to verify refactored code."""

import sys
import traceback

def test_base_router_import():
    """Test that base router can be imported."""
    try:
        from app.api.base.base_router import BaseRouter, BaseCRUDRouter
        assert BaseRouter is not None
        assert BaseCRUDRouter is not None
        print("✓ test_base_router_import: PASSED")
        return True
    except Exception as e:
        print(f"✗ test_base_router_import: FAILED - {e}")
        traceback.print_exc()
        return False

def test_base_service_import():
    """Test that base service can be imported."""
    try:
        from app.services.base.base_service import BaseService, LegacyServiceAdapter
        assert BaseService is not None
        assert LegacyServiceAdapter is not None
        print("✓ test_base_service_import: PASSED")
        return True
    except Exception as e:
        print(f"✗ test_base_service_import: FAILED - {e}")
        traceback.print_exc()
        return False

def test_refactored_bot_router_import():
    """Test that refactored bot router can be imported."""
    try:
        from app.api.v1.bot import router
        assert router is not None
        assert hasattr(router, 'routes')
        
        # Check that CRUD routes are present
        route_paths = [route.path for route in router.routes]
        assert "/bot/" in route_paths
        assert "/bot/{item_id}" in route_paths
        print("✓ test_refactored_bot_router_import: PASSED")
        return True
    except Exception as e:
        print(f"✗ test_refactored_bot_router_import: FAILED - {e}")
        traceback.print_exc()
        return False

def test_refactored_cat_router_import():
    """Test that refactored cat router can be imported."""
    try:
        from app.api.v1.cat import router
        assert router is not None
        assert hasattr(router, 'routes')
        
        # Check that CRUD routes are present
        route_paths = [route.path for route in router.routes]
        assert "/cat/" in route_paths
        assert "/cat/{item_id}" in route_paths
        print("✓ test_refactored_cat_router_import: PASSED")
        return True
    except Exception as e:
        print(f"✗ test_refactored_cat_router_import: FAILED - {e}")
        traceback.print_exc()
        return False

def test_hello_router_import():
    """Test that hello router can be imported."""
    try:
        from app.api.v1.hello import router
        assert router is not None
        assert hasattr(router, 'routes')
        print("✓ test_hello_router_import: PASSED")
        return True
    except Exception as e:
        print(f"✗ test_hello_router_import: FAILED - {e}")
        traceback.print_exc()
        return False

def test_v1_router_import():
    """Test that v1 router includes all sub-routers."""
    try:
        from app.api.v1 import v1_router
        assert v1_router is not None
        
        # Check that all routers are included
        assert len(v1_router.routes) >= 4  # bot, cat, cat_image, hello
        print("✓ test_v1_router_import: PASSED")
        return True
    except Exception as e:
        print(f"✗ test_v1_router_import: FAILED - {e}")
        traceback.print_exc()
        return False

def test_main_app_import():
    """Test that the main app can be imported successfully."""
    try:
        from app.main import app
        assert app is not None
        print("✓ test_main_app_import: PASSED")
        return True
    except Exception as e:
        print(f"✗ test_main_app_import: FAILED - {e}")
        traceback.print_exc()
        return False

def main():
    """Run all import tests."""
    print("Running import tests for refactored FastAPI code...")
    print("=" * 60)
    
    tests = [
        test_base_router_import,
        test_base_service_import,
        test_refactored_bot_router_import,
        test_refactored_cat_router_import,
        test_hello_router_import,
        test_v1_router_import,
        test_main_app_import,
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print("=" * 60)
    print(f"Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All import tests passed!")
        return 0
    else:
        print(f"❌ {total - passed} tests failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())