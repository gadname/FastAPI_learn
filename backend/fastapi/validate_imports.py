#!/usr/bin/env python3
"""Validate all imports match the test requirements."""

import sys
import os
import traceback
from pathlib import Path

# Add the current directory to the Python path
sys.path.insert(0, os.getcwd())

def run_test_base_router_import():
    """Test that base router can be imported."""
    print("Testing base router import...")
    try:
        from app.api.base.base_router import BaseRouter, BaseCRUDRouter
        assert BaseRouter is not None
        assert BaseCRUDRouter is not None
        print("  ✓ BaseRouter and BaseCRUDRouter imported successfully")
        return True
    except Exception as e:
        print(f"  ✗ Failed to import base router: {e}")
        traceback.print_exc()
        return False

def run_test_base_service_import():
    """Test that base service can be imported."""
    print("Testing base service import...")
    try:
        from app.services.base.base_service import BaseService, LegacyServiceAdapter
        assert BaseService is not None
        assert LegacyServiceAdapter is not None
        print("  ✓ BaseService and LegacyServiceAdapter imported successfully")
        return True
    except Exception as e:
        print(f"  ✗ Failed to import base service: {e}")
        traceback.print_exc()
        return False

def run_test_refactored_bot_router_import():
    """Test that refactored bot router can be imported."""
    print("Testing refactored bot router import...")
    try:
        from app.api.v1.bot import router
        assert router is not None
        assert hasattr(router, 'routes')
        
        # Check that CRUD routes are present
        route_paths = [route.path for route in router.routes]
        print(f"  Bot router paths: {route_paths}")
        assert "/bot/" in route_paths
        assert "/bot/{item_id}" in route_paths
        print("  ✓ Bot router imported with correct CRUD routes")
        return True
    except Exception as e:
        print(f"  ✗ Failed to import bot router: {e}")
        traceback.print_exc()
        return False

def run_test_refactored_cat_router_import():
    """Test that refactored cat router can be imported."""
    print("Testing refactored cat router import...")
    try:
        from app.api.v1.cat import router
        assert router is not None
        assert hasattr(router, 'routes')
        
        # Check that CRUD routes are present
        route_paths = [route.path for route in router.routes]
        print(f"  Cat router paths: {route_paths}")
        assert "/cat/" in route_paths
        assert "/cat/{item_id}" in route_paths
        print("  ✓ Cat router imported with correct CRUD routes")
        return True
    except Exception as e:
        print(f"  ✗ Failed to import cat router: {e}")
        traceback.print_exc()
        return False

def run_test_hello_router_import():
    """Test that hello router can be imported."""
    print("Testing hello router import...")
    try:
        from app.api.v1.hello import router
        assert router is not None
        assert hasattr(router, 'routes')
        
        route_paths = [route.path for route in router.routes]
        print(f"  Hello router paths: {route_paths}")
        print("  ✓ Hello router imported successfully")
        return True
    except Exception as e:
        print(f"  ✗ Failed to import hello router: {e}")
        traceback.print_exc()
        return False

def run_test_v1_router_import():
    """Test that v1 router includes all sub-routers."""
    print("Testing v1 router import...")
    try:
        from app.api.v1 import v1_router
        assert v1_router is not None
        
        # Check that all routers are included
        total_routes = len(v1_router.routes)
        print(f"  V1 router has {total_routes} routes")
        assert total_routes >= 4  # bot, cat, cat_image, hello
        print("  ✓ V1 router imported with all sub-routers")
        return True
    except Exception as e:
        print(f"  ✗ Failed to import v1 router: {e}")
        traceback.print_exc()
        return False

def run_test_main_app_import():
    """Test that the main app can be imported successfully."""
    print("Testing main app import...")
    try:
        from app.main import app
        assert app is not None
        print("  ✓ Main FastAPI app imported successfully")
        return True
    except Exception as e:
        print(f"  ✗ Failed to import main app: {e}")
        traceback.print_exc()
        return False

def main():
    """Run all import validation tests."""
    print("Validating imports for refactored FastAPI code...")
    print("=" * 80)
    
    # List of test functions
    tests = [
        ("Base Router Import", run_test_base_router_import),
        ("Base Service Import", run_test_base_service_import),
        ("Refactored Bot Router Import", run_test_refactored_bot_router_import),
        ("Refactored Cat Router Import", run_test_refactored_cat_router_import),
        ("Hello Router Import", run_test_hello_router_import),
        ("V1 Router Import", run_test_v1_router_import),
        ("Main App Import", run_test_main_app_import),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\nRunning: {test_name}")
        print("-" * 40)
        if test_func():
            passed += 1
            print(f"✓ {test_name}: PASSED")
        else:
            print(f"✗ {test_name}: FAILED")
    
    print("\n" + "=" * 80)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All import validation tests passed!")
        print("✓ The refactored code can be imported correctly")
        return 0
    else:
        print(f"❌ {total - passed} import validation tests failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())