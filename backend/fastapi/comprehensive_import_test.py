#!/usr/bin/env python3
"""
Comprehensive import test that mimics the pytest test_imports.py behavior.
This script tests all the imports that would be tested by the pytest file.
"""

import sys
import os
from pathlib import Path

# Add the current directory to Python path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

def test_base_router_import():
    """Test that base router can be imported."""
    print("Testing base router import...")
    try:
        from app.api.base.base_router import BaseRouter, BaseCRUDRouter
        assert BaseRouter is not None
        assert BaseCRUDRouter is not None
        print("  ✓ BaseRouter and BaseCRUDRouter imported successfully")
        return True
    except Exception as e:
        print(f"  ✗ Failed: {e}")
        return False

def test_base_service_import():
    """Test that base service can be imported."""
    print("Testing base service import...")
    try:
        from app.services.base.base_service import BaseService, LegacyServiceAdapter
        assert BaseService is not None
        assert LegacyServiceAdapter is not None
        print("  ✓ BaseService and LegacyServiceAdapter imported successfully")
        return True
    except Exception as e:
        print(f"  ✗ Failed: {e}")
        return False

def test_refactored_bot_router_import():
    """Test that refactored bot router can be imported."""
    print("Testing refactored bot router import...")
    try:
        from app.api.v1.bot import router
        assert router is not None
        assert hasattr(router, 'routes')
        
        # Check that CRUD routes are present
        route_paths = [route.path for route in router.routes]
        print(f"  Bot router paths: {route_paths}")
        
        # Check specific routes
        required_paths = ["/bot/", "/bot/{item_id}"]
        for path in required_paths:
            if path not in route_paths:
                print(f"  ✗ Missing required route: {path}")
                return False
        
        print("  ✓ Bot router with CRUD routes imported successfully")
        return True
    except Exception as e:
        print(f"  ✗ Failed: {e}")
        return False

def test_refactored_cat_router_import():
    """Test that refactored cat router can be imported."""
    print("Testing refactored cat router import...")
    try:
        from app.api.v1.cat import router
        assert router is not None
        assert hasattr(router, 'routes')
        
        # Check that CRUD routes are present
        route_paths = [route.path for route in router.routes]
        print(f"  Cat router paths: {route_paths}")
        
        # Check specific routes
        required_paths = ["/cat/", "/cat/{item_id}"]
        for path in required_paths:
            if path not in route_paths:
                print(f"  ✗ Missing required route: {path}")
                return False
        
        print("  ✓ Cat router with CRUD routes imported successfully")
        return True
    except Exception as e:
        print(f"  ✗ Failed: {e}")
        return False

def test_hello_router_import():
    """Test that hello router can be imported."""
    print("Testing hello router import...")
    try:
        from app.api.v1.hello import router
        assert router is not None
        assert hasattr(router, 'routes')
        print("  ✓ Hello router imported successfully")
        return True
    except Exception as e:
        print(f"  ✗ Failed: {e}")
        return False

def test_v1_router_import():
    """Test that v1 router includes all sub-routers."""
    print("Testing v1 router import...")
    try:
        from app.api.v1 import v1_router
        assert v1_router is not None
        
        # Check that all routers are included
        route_count = len(v1_router.routes)
        print(f"  V1 router has {route_count} routes")
        
        # Should have at least 4 routes (bot, cat, cat_image, hello)
        if route_count < 4:
            print(f"  ✗ Expected at least 4 routes, got {route_count}")
            return False
        
        print("  ✓ V1 router with all sub-routers imported successfully")
        return True
    except Exception as e:
        print(f"  ✗ Failed: {e}")
        return False

def test_main_app_import():
    """Test that the main app can be imported successfully."""
    print("Testing main app import...")
    try:
        from app.main import app
        assert app is not None
        print("  ✓ Main FastAPI app imported successfully")
        return True
    except Exception as e:
        print(f"  ✗ Failed: {e}")
        return False

def run_all_tests():
    """Run all import tests."""
    print("Running comprehensive import tests...")
    print("=" * 80)
    
    tests = [
        ("Base Router Import", test_base_router_import),
        ("Base Service Import", test_base_service_import),
        ("Refactored Bot Router Import", test_refactored_bot_router_import),
        ("Refactored Cat Router Import", test_refactored_cat_router_import),
        ("Hello Router Import", test_hello_router_import),
        ("V1 Router Import", test_v1_router_import),
        ("Main App Import", test_main_app_import),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{test_name}:")
        print("-" * 50)
        if test_func():
            passed += 1
            print(f"RESULT: ✓ PASSED")
        else:
            print(f"RESULT: ✗ FAILED")
    
    print("\n" + "=" * 80)
    print(f"Test Summary: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All import tests passed!")
        print("✓ The refactored code can be imported correctly")
        return 0
    else:
        print(f"❌ {total - passed} import tests failed")
        return 1

if __name__ == "__main__":
    exit_code = run_all_tests()
    print(f"\nExit code: {exit_code}")
    sys.exit(exit_code)