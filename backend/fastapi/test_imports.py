#!/usr/bin/env python3
"""Import validation test script."""

import sys
import traceback

def test_import(import_statement, description):
    """Test a single import statement."""
    print(f"\nTesting {description}:")
    try:
        exec(import_statement)
        print(f"✓ {description} imported successfully")
        return True
    except Exception as e:
        print(f"✗ Import failed: {str(e)}")
        print(f"  Import statement: {import_statement}")
        traceback.print_exc()
        return False

def main():
    """Run all import tests."""
    print("=" * 60)
    print("Import Validation Tests")
    print("=" * 60)
    
    tests = [
        ("from app.api.base.base_router import BaseRouter, BaseCRUDRouter", "BaseRouter and BaseCRUDRouter"),
        ("from app.services.base.base_service import BaseService, LegacyServiceAdapter", "BaseService and LegacyServiceAdapter"),
        ("from app.api.v1.bot import router as bot_router", "bot_router"),
        ("from app.api.v1.cat import router as cat_router", "cat_router"),
        ("from app.api.v1.hello import router as hello_router", "hello_router"),
        ("from app.api.v1 import v1_router", "v1_router"),
    ]
    
    passed = 0
    failed = 0
    
    for import_stmt, description in tests:
        if test_import(import_stmt, description):
            passed += 1
        else:
            failed += 1
    
    print("\n" + "=" * 60)
    print(f"Test Results: {passed} passed, {failed} failed")
    print("=" * 60)
    
    if failed > 0:
        sys.exit(1)
    else:
        print("All imports successful!")

if __name__ == "__main__":
    main()