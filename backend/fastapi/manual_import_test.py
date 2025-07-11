#!/usr/bin/env python3
"""Manual import validation by checking file structure and dependencies."""

import os
import sys
from pathlib import Path

def check_file_exists(filepath: str) -> bool:
    """Check if a file exists."""
    return Path(filepath).exists()

def check_import_dependencies(filepath: str) -> tuple[bool, list[str]]:
    """Check if all imports in a file can be resolved."""
    missing_deps = []
    
    if not check_file_exists(filepath):
        return False, [f"File not found: {filepath}"]
    
    try:
        with open(filepath, 'r') as f:
            content = f.read()
        
        # Simple check for local imports
        lines = content.split('\n')
        for line in lines:
            line = line.strip()
            if line.startswith('from app.'):
                # Extract the module path
                parts = line.split()
                if len(parts) >= 2:
                    module_path = parts[1]
                    # Convert to file path
                    file_path = module_path.replace('.', '/') + '.py'
                    if not check_file_exists(file_path):
                        missing_deps.append(f"Missing dependency: {module_path} ({file_path})")
        
        return len(missing_deps) == 0, missing_deps
    except Exception as e:
        return False, [f"Error reading file: {str(e)}"]

def main():
    """Run manual import validation."""
    print("=" * 60)
    print("Manual Import Validation")
    print("=" * 60)
    
    # Change to the correct directory
    os.chdir('/home/runner/work/FastAPI_learn/FastAPI_learn/backend/fastapi')
    
    # List of files to check and their expected imports
    files_to_check = [
        ("app/api/base/base_router.py", "BaseRouter, BaseCRUDRouter"),
        ("app/services/base/base_service.py", "BaseService, LegacyServiceAdapter"),
        ("app/api/v1/bot.py", "bot_router"),
        ("app/api/v1/cat.py", "cat_router"),
        ("app/api/v1/hello.py", "hello_router"),
        ("app/api/v1/__init__.py", "v1_router"),
    ]
    
    results = []
    
    for filepath, description in files_to_check:
        print(f"\nChecking {description}:")
        print(f"  File: {filepath}")
        
        if check_file_exists(filepath):
            print(f"  ✓ File exists")
            
            # Check dependencies
            deps_ok, missing_deps = check_import_dependencies(filepath)
            if deps_ok:
                print(f"  ✓ All dependencies appear to be available")
                results.append((description, True, None))
            else:
                print(f"  ✗ Missing dependencies:")
                for dep in missing_deps:
                    print(f"    - {dep}")
                results.append((description, False, missing_deps))
        else:
            print(f"  ✗ File not found")
            results.append((description, False, ["File not found"]))
    
    print("\n" + "=" * 60)
    print("Summary:")
    print("=" * 60)
    
    passed = 0
    failed = 0
    
    for description, success, errors in results:
        if success:
            print(f"✓ {description}")
            passed += 1
        else:
            print(f"✗ {description}")
            failed += 1
            if errors:
                for error in errors:
                    print(f"  - {error}")
    
    print(f"\nResults: {passed} passed, {failed} failed")
    
    # Check for __init__.py files in directories
    print("\n" + "=" * 60)
    print("Checking __init__.py files:")
    print("=" * 60)
    
    init_files = [
        "app/__init__.py",
        "app/api/__init__.py",
        "app/api/base/__init__.py",
        "app/api/v1/__init__.py",
        "app/services/__init__.py",
        "app/services/base/__init__.py",
    ]
    
    for init_file in init_files:
        if check_file_exists(init_file):
            print(f"✓ {init_file}")
        else:
            print(f"✗ {init_file} (may cause import issues)")

if __name__ == "__main__":
    main()