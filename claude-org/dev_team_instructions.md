# 6ペイン開発チーム運営マニュアル

## チーム構成（3x2レイアウト）

```
👑 Boss      📋 PM
🎨 Frontend  ⚙️ Backend  
🚀 Fullstack 🧪 Test
```

## 各開発者の専門分野と役割

### 🎨 Frontend Developer
**専門技術:** React, Next.js, TypeScript, CSS, UI/UX
**担当領域:**
- ユーザーインターフェース設計・実装
- レスポンシブデザイン
- フロントエンドライブラリの選定・実装
- ユーザー体験の最適化

### ⚙️ Backend Developer  
**専門技術:** FastAPI, Python, SQLAlchemy, PostgreSQL/SQLite
**担当領域:**
- REST API設計・実装
- データベース設計・最適化
- 認証・認可システム
- パフォーマンス最適化

### 🚀 Fullstack Developer
**専門技術:** フロント・バック統合, Docker, CI/CD, デプロイ
**担当領域:**
- フロントエンドとバックエンドの統合
- デプロイメント戦略
- 開発環境・本番環境構築
- 全体アーキテクチャの統括

## 実践的な指示出し例

### Phase 1: プロジェクト開始 (Boss → PM)

```markdown
# Webアプリケーション開発プロジェクト

## 概要
タスク管理Webアプリケーションの開発

## 要件
- **フロントエンド**: Next.js + TypeScript
- **バックエンド**: FastAPI + SQLite  
- **機能**: タスクのCRUD、ユーザー認証、リアルタイム更新

## 期待する成果物
各開発者への具体的なタスク分割と技術仕様書
```

### Phase 2: 技術仕様決定 (PM → 各開発者)

#### PM → Frontend Developer
```markdown
# フロントエンド技術仕様

## タスク
Next.jsベースのタスク管理UIの実装

## 要件
- TypeScript必須
- Tailwind CSS使用
- React Query/SWRでデータフェッチ
- レスポンシブデザイン対応

## ページ構成
1. ログイン・サインアップページ
2. ダッシュボード（タスク一覧）
3. タスク詳細・編集ページ

## API連携
バックエンド開発者が提供するAPI仕様に従って実装
```

#### PM → Backend Developer
```markdown
# バックエンド技術仕様

## タスク  
FastAPIベースのREST API実装

## 要件
- JWT認証システム
- SQLAlchemyでのORM
- Pydanticでのバリデーション
- 自動生成されるSwagger UI

## APIエンドポイント
- POST /auth/login, /auth/register
- GET, POST, PUT, DELETE /tasks
- GET /users/me

## データベース設計
User, Task テーブルの設計と実装
```

#### PM → Fullstack Developer
```markdown
# フルスタック統合仕様

## タスク
フロントエンドとバックエンドの統合・デプロイ

## 要件
- Docker Compose環境構築
- CORS設定の最適化
- 環境変数管理
- CI/CDパイプライン構築

## 成果物
- docker-compose.yml
- 本番環境用Dockerfile
- GitHub Actionsワークフロー
```

## 開発フロー例

### ステップ1: 環境起動
```bash
./claude-org/setup_6pane_dev_team.sh
```

### ステップ2: 各ペインでClaude Code起動
```bash
# 各開発者ペインで実行
claude
```

### ステップ3: 並行開発開始

1. **Frontend Developer** が UI コンポーネント開発開始
2. **Backend Developer** が API エンドポイント開発開始  
3. **Fullstack Developer** が開発環境構築開始

### ステップ4: 統合・テスト

1. **Backend** が API 完成を報告
2. **Frontend** が API 連携を実装
3. **Fullstack** が統合テスト実行
4. **Test** が品質保証実行

## 効果的な連携パターン

### 技術的な質問・相談
```
Frontend → Backend: 「APIのレスポンス形式について確認したい」
Backend → Frontend: 「このUI要件をAPIでどう実現するか相談したい」
```

### 問題解決の連携
```
Backend Developer: 「PostgreSQLの接続でエラーが発生している」
→ Fullstack Developer: 「docker-compose.ymlの設定を確認します」
```

### Web検索の活用例
```
Frontend Developer: 「Next.js 14の新しいApp Routerでの認証実装方法を調べてください」
Backend Developer: 「FastAPIでのJWT refresh token実装のベストプラクティスを検索してください」
```

## 成功のポイント

### 1. 明確な責任分界
- 各開発者の専門領域を明確に分ける
- オーバーラップする部分は事前に調整

### 2. 継続的なコミュニケーション
- API 仕様の変更は即座に共有
- 進捗の定期報告

### 3. 段階的な統合
- 小さな機能単位で統合テスト
- 問題の早期発見・修正

### 4. ドキュメント化
- 技術仕様書の継続的な更新
- 決定事項の記録・共有