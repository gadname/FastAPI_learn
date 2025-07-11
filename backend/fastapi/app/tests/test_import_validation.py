import pytest
import importlib
import sys
from pathlib import Path


class TestImportValidation:
    """Test that all modules can be imported successfully"""
    
    def test_import_base_router(self):
        """Test that the base router module can be imported"""
        try:
            from app.api.base.base_router import BaseRouter, BaseCRUDRouter
            assert BaseRouter is not None
            assert BaseCRUDRouter is not None
        except ImportError as e:
            pytest.fail(f"Failed to import base router: {e}")
    
    def test_import_base_service(self):
        """Test that the base service module can be imported"""
        try:
            from app.services.base.base_service import BaseService, LegacyServiceAdapter, BaseCRUDService
            assert BaseService is not None
            assert LegacyServiceAdapter is not None
            assert BaseCRUDService is not None
        except ImportError as e:
            pytest.fail(f"Failed to import base service: {e}")
    
    def test_import_refactored_bot_router(self):
        """Test that the refactored bot router can be imported"""
        try:
            from app.api.v1.bot import router as bot_router
            assert bot_router is not None
        except ImportError as e:
            pytest.fail(f"Failed to import refactored bot router: {e}")
    
    def test_import_refactored_cat_router(self):
        """Test that the refactored cat router can be imported"""
        try:
            from app.api.v1.cat import router as cat_router
            assert cat_router is not None
        except ImportError as e:
            pytest.fail(f"Failed to import refactored cat router: {e}")
    
    def test_import_hello_router(self):
        """Test that the hello router can be imported"""
        try:
            from app.api.v1.hello import router as hello_router
            assert hello_router is not None
        except ImportError as e:
            pytest.fail(f"Failed to import hello router: {e}")
    
    def test_import_v1_router(self):
        """Test that the v1 router with all registrations can be imported"""
        try:
            from app.api.v1 import v1_router
            assert v1_router is not None
        except ImportError as e:
            pytest.fail(f"Failed to import v1 router: {e}")
    
    def test_import_existing_services(self):
        """Test that existing services can still be imported"""
        try:
            from app.services.chat_bot import ChatBotService
            from app.services.cat import CatService
            from app.services.cat_image import CatImageService
            
            assert ChatBotService is not None
            assert CatService is not None
            assert CatImageService is not None
        except ImportError as e:
            pytest.fail(f"Failed to import existing services: {e}")
    
    def test_import_schemas(self):
        """Test that all schemas can be imported"""
        try:
            from app.schemas.bot import BotCreate, BotResponse, BotAllResponse
            from app.schemas.cat import CatCreate, CatResponse, CatAllResponse
            from app.schemas.cat_image import CatImageResponse
            
            assert BotCreate is not None
            assert BotResponse is not None
            assert BotAllResponse is not None
            assert CatCreate is not None
            assert CatResponse is not None
            assert CatAllResponse is not None
            assert CatImageResponse is not None
        except ImportError as e:
            pytest.fail(f"Failed to import schemas: {e}")
    
    def test_syntax_validation(self):
        """Test that all Python files have valid syntax"""
        test_files = [
            "app/api/base/base_router.py",
            "app/services/base/base_service.py",
            "app/api/v1/bot.py",
            "app/api/v1/cat.py",
            "app/api/v1/__init__.py",
        ]
        
        for file_path in test_files:
            try:
                # Try to compile the file
                with open(file_path, 'r') as f:
                    content = f.read()
                compile(content, file_path, 'exec')
            except SyntaxError as e:
                pytest.fail(f"Syntax error in {file_path}: {e}")
            except FileNotFoundError:
                pytest.fail(f"File not found: {file_path}")
    
    def test_circular_import_detection(self):
        """Test that there are no circular imports"""
        try:
            # Try importing all modules in sequence
            from app.api.base import base_router
            from app.services.base import base_service
            from app.api.v1 import bot, cat, hello
            from app.api.v1 import v1_router
            
            # If we get here without errors, no circular imports detected
            assert True
        except ImportError as e:
            pytest.fail(f"Circular import detected: {e}")