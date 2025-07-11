#!/usr/bin/env python3
"""Direct import validation test."""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.getcwd())

print("=" * 70)
print("DIRECT IMPORT VALIDATION TEST")
print("=" * 70)

passed = 0
failed = 0

# Test 1: BaseRouter and BaseCRUDRouter
print("\nTest 1: BaseRouter and BaseCRUDRouter")
try:
    from app.api.base.base_router import BaseRouter, BaseCRUDRouter
    print("  ✓ SUCCESS: BaseRouter and BaseCRUDRouter imported successfully")
    passed += 1
except Exception as e:
    print(f"  ✗ FAILED: {str(e)}")
    failed += 1

# Test 2: BaseService and LegacyServiceAdapter
print("\nTest 2: BaseService and LegacyServiceAdapter")
try:
    from app.services.base.base_service import BaseService, LegacyServiceAdapter
    print("  ✓ SUCCESS: BaseService and LegacyServiceAdapter imported successfully")
    passed += 1
except Exception as e:
    print(f"  ✗ FAILED: {str(e)}")
    failed += 1

# Test 3: bot_router
print("\nTest 3: bot_router")
try:
    from app.api.v1.bot import router as bot_router
    print("  ✓ SUCCESS: bot_router imported successfully")
    passed += 1
except Exception as e:
    print(f"  ✗ FAILED: {str(e)}")
    failed += 1

# Test 4: cat_router
print("\nTest 4: cat_router")
try:
    from app.api.v1.cat import router as cat_router
    print("  ✓ SUCCESS: cat_router imported successfully")
    passed += 1
except Exception as e:
    print(f"  ✗ FAILED: {str(e)}")
    failed += 1

# Test 5: hello_router
print("\nTest 5: hello_router")
try:
    from app.api.v1.hello import router as hello_router
    print("  ✓ SUCCESS: hello_router imported successfully")
    passed += 1
except Exception as e:
    print(f"  ✗ FAILED: {str(e)}")
    failed += 1

# Test 6: v1_router
print("\nTest 6: v1_router")
try:
    from app.api.v1 import v1_router
    print("  ✓ SUCCESS: v1_router imported successfully")
    passed += 1
except Exception as e:
    print(f"  ✗ FAILED: {str(e)}")
    failed += 1

print("\n" + "=" * 70)
print("RESULTS")
print("=" * 70)
print(f"Passed: {passed}")
print(f"Failed: {failed}")
print(f"Total:  {passed + failed}")

if failed == 0:
    print("\n🎉 ALL IMPORTS SUCCESSFUL!")
else:
    print(f"\n❌ {failed} IMPORTS FAILED!")

sys.exit(0 if failed == 0 else 1)