"""Test that all imports work correctly after refactoring."""

import pytest


def test_base_router_import():
    """Test that base router can be imported."""
    from app.api.base.base_router import BaseRouter, BaseCRUDRouter
    assert BaseRouter is not None
    assert BaseCRUDRouter is not None


def test_base_service_import():
    """Test that base service can be imported."""
    from app.services.base.base_service import BaseService, LegacyServiceAdapter
    assert BaseService is not None
    assert LegacyServiceAdapter is not None


def test_refactored_bot_router_import():
    """Test that refactored bot router can be imported."""
    from app.api.v1.bot import router
    assert router is not None
    assert hasattr(router, 'routes')
    
    # Check that CRUD routes are present
    route_paths = [route.path for route in router.routes]
    assert "/bot/" in route_paths
    assert "/bot/{item_id}" in route_paths


def test_refactored_cat_router_import():
    """Test that refactored cat router can be imported."""
    from app.api.v1.cat import router
    assert router is not None
    assert hasattr(router, 'routes')
    
    # Check that CRUD routes are present
    route_paths = [route.path for route in router.routes]
    assert "/cat/" in route_paths
    assert "/cat/{item_id}" in route_paths


def test_hello_router_import():
    """Test that hello router can be imported."""
    from app.api.v1.hello import router
    assert router is not None
    assert hasattr(router, 'routes')


def test_v1_router_import():
    """Test that v1 router includes all sub-routers."""
    from app.api.v1 import v1_router
    assert v1_router is not None
    
    # Check that all routers are included
    assert len(v1_router.routes) >= 4  # bot, cat, cat_image, hello


def test_main_app_import():
    """Test that the main app can be imported successfully."""
    from app.main import app
    assert app is not None