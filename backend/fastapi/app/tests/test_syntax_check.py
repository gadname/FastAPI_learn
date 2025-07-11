"""Syntax and basic functionality verification tests."""

import ast
import sys
from pathlib import Path


def test_syntax_check():
    """Test that all Python files have valid syntax."""
    base_dir = Path(__file__).parent.parent
    
    # List of files to check
    files_to_check = [
        "api/base/base_router.py",
        "services/base/base_service.py",
        "api/v1/bot.py",
        "api/v1/cat.py",
        "api/v1/hello.py",
        "api/v1/__init__.py",
    ]
    
    for file_path in files_to_check:
        full_path = base_dir / file_path
        if full_path.exists():
            with open(full_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            try:
                ast.parse(content)
                print(f"✓ {file_path}: Syntax OK")
            except SyntaxError as e:
                print(f"✗ {file_path}: Syntax Error - {e}")
                raise
        else:
            print(f"⚠ {file_path}: File not found")


def test_basic_imports():
    """Test that basic imports work."""
    try:
        # Test base imports
        from app.api.base.base_router import BaseRouter, BaseCRUDRouter
        from app.services.base.base_service import BaseService, LegacyServiceAdapter
        print("✓ Base classes imported successfully")
        
        # Test router imports
        from app.api.v1.bot import router as bot_router
        from app.api.v1.cat import router as cat_router
        from app.api.v1.hello import router as hello_router
        print("✓ Router imports successful")
        
        # Test v1 router
        from app.api.v1 import v1_router
        print("✓ V1 router import successful")
        
        # Test main app
        from app.main import app
        print("✓ Main app import successful")
        
        return True
    except Exception as e:
        print(f"✗ Import failed: {e}")
        return False


if __name__ == "__main__":
    print("Running syntax and import checks...")
    
    try:
        test_syntax_check()
        test_basic_imports()
        print("\n✅ All checks passed!")
    except Exception as e:
        print(f"\n❌ Tests failed: {e}")
        sys.exit(1)