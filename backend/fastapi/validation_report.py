#!/usr/bin/env python3
"""
Import Validation Report Generator
This script analyzes the file structure and dependencies to predict import success.
"""

import os
from pathlib import Path

# Define the base directory
BASE_DIR = Path("/home/runner/work/FastAPI_learn/FastAPI_learn/backend/fastapi")

def check_file_exists(filepath: str) -> bool:
    """Check if a file exists."""
    full_path = BASE_DIR / filepath
    return full_path.exists()

def analyze_imports():
    """Analyze import requirements and file structure."""
    print("=" * 70)
    print("IMPORT VALIDATION REPORT")
    print("=" * 70)
    
    # List of imports to validate
    imports_to_check = [
        {
            "import": "from app.api.base.base_router import BaseRouter, BaseCRUDRouter",
            "description": "BaseRouter, BaseCRUDRouter",
            "file": "app/api/base/base_router.py",
            "classes": ["BaseRouter", "BaseCRUDRouter"]
        },
        {
            "import": "from app.services.base.base_service import BaseService, LegacyServiceAdapter",
            "description": "BaseService, LegacyServiceAdapter",
            "file": "app/services/base/base_service.py",
            "classes": ["BaseService", "LegacyServiceAdapter"]
        },
        {
            "import": "from app.api.v1.bot import router as bot_router",
            "description": "bot_router",
            "file": "app/api/v1/bot.py",
            "classes": ["router"]
        },
        {
            "import": "from app.api.v1.cat import router as cat_router",
            "description": "cat_router",
            "file": "app/api/v1/cat.py",
            "classes": ["router"]
        },
        {
            "import": "from app.api.v1.hello import router as hello_router",
            "description": "hello_router",
            "file": "app/api/v1/hello.py",
            "classes": ["router"]
        },
        {
            "import": "from app.api.v1 import v1_router",
            "description": "v1_router",
            "file": "app/api/v1/__init__.py",
            "classes": ["v1_router"]
        }
    ]
    
    # Required __init__.py files
    required_init_files = [
        "app/__init__.py",
        "app/api/__init__.py",
        "app/api/base/__init__.py",
        "app/api/v1/__init__.py",
        "app/services/__init__.py",
        "app/services/base/__init__.py",
    ]
    
    # Check __init__.py files
    print("\n1. CHECKING __init__.py FILES:")
    print("-" * 40)
    init_files_ok = True
    for init_file in required_init_files:
        if check_file_exists(init_file):
            print(f"  ✓ {init_file}")
        else:
            print(f"  ✗ {init_file} (MISSING - will cause import errors)")
            init_files_ok = False
    
    # Check main files
    print("\n2. CHECKING MAIN FILES:")
    print("-" * 40)
    files_ok = True
    for item in imports_to_check:
        if check_file_exists(item["file"]):
            print(f"  ✓ {item['file']}")
        else:
            print(f"  ✗ {item['file']} (MISSING)")
            files_ok = False
    
    # Check content of files
    print("\n3. CHECKING FILE CONTENT:")
    print("-" * 40)
    content_ok = True
    for item in imports_to_check:
        if check_file_exists(item["file"]):
            try:
                with open(BASE_DIR / item["file"], 'r') as f:
                    content = f.read()
                
                # Check if expected classes/variables are defined
                missing_classes = []
                for class_name in item["classes"]:
                    if class_name not in content:
                        missing_classes.append(class_name)
                
                if missing_classes:
                    print(f"  ✗ {item['file']}: Missing {', '.join(missing_classes)}")
                    content_ok = False
                else:
                    print(f"  ✓ {item['file']}: All expected items found")
            except Exception as e:
                print(f"  ✗ {item['file']}: Error reading file - {str(e)}")
                content_ok = False
        else:
            print(f"  ✗ {item['file']}: File not found")
            content_ok = False
    
    # Summary
    print("\n4. IMPORT PREDICTION:")
    print("-" * 40)
    success_count = 0
    for item in imports_to_check:
        if check_file_exists(item["file"]):
            try:
                with open(BASE_DIR / item["file"], 'r') as f:
                    content = f.read()
                
                # Simple check for expected content
                all_found = all(class_name in content for class_name in item["classes"])
                if all_found and init_files_ok:
                    print(f"  ✓ {item['description']} - LIKELY SUCCESS")
                    success_count += 1
                else:
                    print(f"  ✗ {item['description']} - LIKELY FAILURE")
            except:
                print(f"  ✗ {item['description']} - LIKELY FAILURE (file error)")
        else:
            print(f"  ✗ {item['description']} - FAILURE (file not found)")
    
    print("\n" + "=" * 70)
    print(f"SUMMARY: {success_count}/{len(imports_to_check)} imports predicted to succeed")
    print("=" * 70)
    
    if success_count == len(imports_to_check):
        print("✓ All imports should work successfully!")
    else:
        print("✗ Some imports may fail. Check the issues above.")
    
    return success_count == len(imports_to_check)

if __name__ == "__main__":
    analyze_imports()