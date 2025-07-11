#!/usr/bin/env python3
"""Run pytest tests programmatically."""

import sys
import os

# Add the current directory to the Python path
sys.path.insert(0, os.getcwd())

try:
    import pytest
    
    # Run the specific test file
    print("Running pytest tests for app/tests/test_imports.py...")
    print("=" * 60)
    
    # Run pytest with the specific test file
    exit_code = pytest.main([
        "app/tests/test_imports.py",
        "-v",
        "--tb=short"
    ])
    
    print("=" * 60)
    if exit_code == 0:
        print("🎉 All pytest tests passed!")
    else:
        print(f"❌ pytest tests failed with exit code {exit_code}")
    
    sys.exit(exit_code)
    
except ImportError:
    print("❌ pytest not available. Running manual tests instead...")
    import test_imports_manual
    sys.exit(test_imports_manual.main())
except Exception as e:
    print(f"❌ Error running pytest: {e}")
    print("Running manual tests instead...")
    import test_imports_manual
    sys.exit(test_imports_manual.main())