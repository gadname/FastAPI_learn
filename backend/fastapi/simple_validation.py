#!/usr/bin/env python3
"""Simple import validation without pytest."""

import sys
import traceback

def test_import(import_statement, description):
    """Test a single import statement."""
    print(f"\nTesting {description}:")
    print(f"  Import: {import_statement}")
    
    try:
        exec(import_statement)
        print(f"  ✓ SUCCESS: {description} imported successfully")
        return True
    except Exception as e:
        print(f"  ✗ FAILED: {description}")
        print(f"    Error: {str(e)}")
        print(f"    Traceback:")
        traceback.print_exc()
        return False

def main():
    """Run import validation tests."""
    print("=" * 70)
    print("IMPORT VALIDATION TEST RESULTS")
    print("=" * 70)
    
    # Test cases based on the pytest file
    tests = [
        ("from app.api.base.base_router import BaseRouter, BaseCRUDRouter", "BaseRouter, BaseCRUDRouter"),
        ("from app.services.base.base_service import BaseService, LegacyServiceAdapter", "BaseService, LegacyServiceAdapter"),
        ("from app.api.v1.bot import router as bot_router", "bot_router"),
        ("from app.api.v1.cat import router as cat_router", "cat_router"),
        ("from app.api.v1.hello import router as hello_router", "hello_router"),
        ("from app.api.v1 import v1_router", "v1_router"),
    ]
    
    passed = 0
    failed = 0
    
    for import_stmt, desc in tests:
        if test_import(import_stmt, desc):
            passed += 1
        else:
            failed += 1
    
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print(f"Total:  {passed + failed}")
    
    if failed == 0:
        print("\n🎉 ALL IMPORTS SUCCESSFUL!")
        return True
    else:
        print(f"\n❌ {failed} IMPORTS FAILED!")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)