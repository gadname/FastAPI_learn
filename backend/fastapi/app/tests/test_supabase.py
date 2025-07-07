import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from app.main import app
from app.settings import settings

client = TestClient(app)


def test_supabase_status_disabled():
    """
    Supabaseが無効の場合のステータス確認
    """
    with patch.object(settings, 'use_supabase', False):
        response = client.get("/api/v1/supabase/status")
        assert response.status_code == 200
        
        data = response.json()
        assert data["enabled"] is False
        assert data["connected"] is False
        assert "disabled" in data["message"].lower()


def test_supabase_status_enabled_no_config():
    """
    Supabaseが有効だが設定が不完全な場合のステータス確認
    """
    with patch.object(settings, 'use_supabase', True):
        with patch.object(settings, 'supabase_url', ""):
            response = client.get("/api/v1/supabase/status")
            assert response.status_code == 200
            
            data = response.json()
            assert data["enabled"] is True
            assert data["connected"] is False


def test_supabase_chat_bots_disabled():
    """
    Supabaseが無効の場合のチャットボット取得
    """
    with patch.object(settings, 'use_supabase', False):
        response = client.get("/api/v1/supabase/chat-bots")
        assert response.status_code == 200
        
        data = response.json()
        assert isinstance(data, list)
        # 空のリストが返される（DBセッションが無いため）
        assert len(data) == 0


def test_supabase_cats_disabled():
    """
    Supabaseが無効の場合の猫取得
    """
    with patch.object(settings, 'use_supabase', False):
        response = client.get("/api/v1/supabase/cats")
        assert response.status_code == 200
        
        data = response.json()
        assert isinstance(data, list)
        # 空のリストが返される（DBセッションが無いため）
        assert len(data) == 0


def test_supabase_create_chat_bot_disabled():
    """
    Supabaseが無効の場合のチャットボット作成
    """
    with patch.object(settings, 'use_supabase', False):
        response = client.post("/api/v1/supabase/chat-bots", json={
            "name": "Test Bot",
            "color": "blue"
        })
        # DBセッションが無いため500エラーが発生
        assert response.status_code == 500


def test_supabase_create_cat_disabled():
    """
    Supabaseが無効の場合の猫作成
    """
    with patch.object(settings, 'use_supabase', False):
        response = client.post("/api/v1/supabase/cats", json={
            "name": "Test Cat",
            "breed": "Persian"
        })
        # DBセッションが無いため500エラーが発生
        assert response.status_code == 500


@pytest.mark.asyncio
async def test_supabase_client_initialization():
    """
    Supabaseクライアントの初期化テスト
    """
    from app.db.supabase_client import get_supabase_client
    
    with patch.object(settings, 'use_supabase', False):
        client = get_supabase_client()
        assert client is None
    
    with patch.object(settings, 'use_supabase', True):
        with patch.object(settings, 'supabase_url', ""):
            client = get_supabase_client()
            assert client is None


@pytest.mark.asyncio
async def test_hybrid_db_service():
    """
    ハイブリッドDBサービスのテスト
    """
    from app.services.hybrid_db import HybridDBService
    
    with patch.object(settings, 'use_supabase', False):
        service = HybridDBService()
        assert service.use_supabase is False
        
        # データベースセッションが無いため空のリストが返される
        chat_bots = await service.get_chat_bots()
        assert chat_bots == []
        
        cats = await service.get_cats()
        assert cats == []