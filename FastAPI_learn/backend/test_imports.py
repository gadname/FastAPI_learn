#!/usr/bin/env python3
"""Test script to verify all imports work correctly."""

print("Testing imports...")

try:
    from main import app
    print("✓ main.app imported successfully")
except ImportError as e:
    print(f"✗ Failed to import main.app: {e}")

try:
    from db.base_class import Base
    print("✓ db.base_class.Base imported successfully")
except ImportError as e:
    print(f"✗ Failed to import db.base_class.Base: {e}")

try:
    from db.session import get_db, engine
    print("✓ db.session imported successfully")
except ImportError as e:
    print(f"✗ Failed to import db.session: {e}")

try:
    from models.cat import Cat
    print("✓ models.cat.Cat imported successfully")
except ImportError as e:
    print(f"✗ Failed to import models.cat.Cat: {e}")

try:
    from schemas.cat import CatCreate, CatUpdate, Cat as CatSchema
    print("✓ schemas.cat imported successfully")
except ImportError as e:
    print(f"✗ Failed to import schemas.cat: {e}")

try:
    from cruds.cat import get_cat, get_cats, create_cat, update_cat, delete_cat
    print("✓ cruds.cat imported successfully")
except ImportError as e:
    print(f"✗ Failed to import cruds.cat: {e}")

try:
    from api.v1.endpoints.cats import router
    print("✓ api.v1.endpoints.cats.router imported successfully")
except ImportError as e:
    print(f"✗ Failed to import api.v1.endpoints.cats.router: {e}")

print("\nAll import tests completed!")
print("\nTo run the application:")
print("1. Install dependencies: pip install -r requirements.txt")
print("2. Run the server: uvicorn main:app --reload")