# Supabase Integration

この実装では、既存のFastAPI + PostgreSQL + Next.jsアプリケーションにSupabaseを段階的に統合します。

## 実装概要

### アーキテクチャ

- **ハイブリッド実装**: 既存のSQLAlchemyとSupabaseクライアントの両方をサポート
- **段階的移行**: 設定でSupabaseの有効/無効を切り替え可能
- **フォールバック機能**: Supabaseが利用できない場合、自動的に従来のSQLAlchemyに切り替え

### 主要コンポーネント

#### Backend (FastAPI)

1. **Supabaseクライアント** (`app/db/supabase_client.py`)
   - Supabaseクライアントの初期化と管理
   - 接続テスト機能

2. **認証サービス** (`app/services/auth.py`)
   - Supabase JWT認証の実装
   - 認証の依存関数

3. **ハイブリッドDBサービス** (`app/services/hybrid_db.py`)
   - SQLAlchemyとSupabaseの両方をサポート
   - 自動フォールバック機能

4. **Supabase API** (`app/api/v1/supabase.py`)
   - Supabase機能のAPIエンドポイント
   - 認証統合のデモンストレーション

#### Frontend (Next.js)

1. **Supabaseクライアント** (`lib/supabase.ts`)
   - クライアントサイドのSupabase操作
   - 認証とCRUD操作のヘルパー関数

## セットアップ

### 1. Supabaseプロジェクトの作成

1. [Supabase](https://supabase.com)でプロジェクトを作成
2. データベースのスキーマを設定
3. 必要に応じてRow Level Security (RLS)を設定

### 2. 環境変数の設定

バックエンドの`.env`ファイルに以下を追加:

```env
# Supabase Configuration
use_supabase=true
supabase_url=https://your-project-id.supabase.co
supabase_key=your-anon-key
supabase_service_role_key=your-service-role-key
```

フロントエンドの環境変数:

```env
NEXT_PUBLIC_SUPABASE_URL=https://your-project-id.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-key
```

### 3. 依存関係のインストール

```bash
# Backend
cd backend/fastapi
poetry install

# Frontend
cd frontend
npm install
```

## 使用方法

### 1. 従来のSQLAlchemyモード

```env
use_supabase=false
```

この設定では、既存のPostgreSQLデータベースを使用します。

### 2. Supabaseモード

```env
use_supabase=true
```

この設定では、Supabaseを優先的に使用し、フォールバック機能も提供します。

### 3. API エンドポイント

#### Supabase状態の確認

```bash
curl http://localhost:8000/api/v1/supabase/status
```

#### チャットボットの操作

```bash
# 一覧取得
curl http://localhost:8000/api/v1/supabase/chat-bots

# 作成
curl -X POST http://localhost:8000/api/v1/supabase/chat-bots \
  -H "Content-Type: application/json" \
  -d '{"name": "Test Bot", "color": "blue"}'
```

## 実装の特徴

### 1. 段階的移行

- 既存のコードを破壊することなく、新しいSupabase機能を追加
- 設定で簡単に切り替え可能

### 2. フォールバック機能

- Supabaseが利用できない場合、自動的にSQLAlchemyに切り替え
- 高可用性を確保

### 3. 認証統合

- Supabase AuthとFastAPIの統合
- JWTトークンベースの認証

### 4. 型安全性

- TypeScriptでの型定義
- Pydanticモデルでのデータ検証

## 今後の拡張

### Phase 2: 認証システムの完全統合

- ユーザー登録・ログイン機能
- プロフィール管理
- 権限ベースのアクセス制御

### Phase 3: リアルタイム機能

- Supabase Realtimeの統合
- WebSocketベースのリアルタイム更新

### Phase 4: ファイルストレージ

- Supabase Storageの統合
- 画像・ファイルのアップロード機能

## セキュリティ

- Row Level Security (RLS)の実装
- 適切な権限管理
- 秘密情報の環境変数管理

## トラブルシューティング

### 接続エラー

1. 環境変数が正しく設定されているか確認
2. Supabaseプロジェクトが正常に動作しているか確認
3. APIキーの権限が適切か確認

### 認証エラー

1. JWTトークンが有効か確認
2. Supabaseのサービスロールキーが正しいか確認
3. 認証設定が正しいか確認

この実装により、既存のアプリケーションを破壊することなく、Supabaseの強力な機能を段階的に導入できます。