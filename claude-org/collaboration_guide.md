# Claude Code開発者間の協調・対話方法

## 1. 基本的な協調パターン

### パターンA: Boss役が仲介する方法（推奨）
```
Frontend → Boss → Backend
Backend → Boss → Frontend
```

**実践例:**
1. Frontend開発者が「APIのレスポンス形式を確認したい」とBoss役に報告
2. Boss役がBackend開発者に「APIレスポンス形式を共有してください」と依頼
3. Backend開発者が仕様を作成
4. Boss役がFrontend開発者に仕様を伝達

### パターンB: 共有ファイル経由での対話
```
Frontend → shared/api_request.md → Backend
Backend → shared/api_response.md → Frontend
```

## 2. 具体的な対話・協調手順

### ステップ1: 共有ディレクトリの準備
```bash
mkdir -p claude-org/shared/{requests,responses,specs,issues}
```

### ステップ2: 対話テンプレートファイルの作成

#### Frontend → Backend への質問例
```markdown
# shared/requests/frontend_to_backend_001.md

## 質問者: Frontend Developer
## 宛先: Backend Developer  
## 日時: 2025-01-XX XX:XX

## 質問内容
タスク一覧取得APIについて確認したいことがあります。

### 1. エンドポイント仕様
- URL: GET /api/tasks
- 必要なクエリパラメータはありますか？

### 2. レスポンス形式
期待するJSON構造を教えてください。特に：
- タスクオブジェクトの構造
- ページネーション情報
- エラー時のレスポンス

### 3. 認証
JWT tokenの送信方法を確認したいです。

## 実装予定
このAPIを使ってReactコンポーネントを実装予定です。

---
回答は shared/responses/backend_to_frontend_001.md に記載してください。
```

#### Backend → Frontend への回答例
```markdown
# shared/responses/backend_to_frontend_001.md

## 回答者: Backend Developer
## 宛先: Frontend Developer
## 日時: 2025-01-XX XX:XX

## 回答内容

### 1. エンドポイント仕様
```
GET /api/tasks?page=1&limit=20&status=pending
```

### 2. レスポンス形式
```json
{
  "tasks": [
    {
      "id": 1,
      "title": "タスクタイトル",
      "description": "説明",
      "status": "pending",
      "created_at": "2025-01-01T00:00:00Z"
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 100
  }
}
```

### 3. 認証
HeaderにBearer tokenを設定：
```
Authorization: Bearer <JWT_TOKEN>
```

## 実装済み
APIは `/api/tasks` で実装済みです。
テスト用のSwagger UIは http://localhost:8000/docs で確認できます。
```

## 3. 実際の協調ワークフロー

### 例: タスク管理アプリの開発

#### Phase 1: 仕様調整
1. **PM役**が全体仕様をshared/specs/project_spec.mdに作成
2. **Frontend・Backend・Fullstack**が各自の担当部分を確認
3. 疑問点をshared/requests/に質問ファイルとして投稿
4. **Boss役**が調整・回答を指示

#### Phase 2: 並行開発
1. **Backend**がAPIエンドポイントを実装
2. **Frontend**がモックデータでUI開発
3. **Fullstack**が開発環境構築

#### Phase 3: 統合
1. **Backend**がAPI仕様書をshared/specs/api_spec.mdに更新
2. **Frontend**が実際のAPIに接続
3. **Fullstack**が統合テスト実行

## 4. 実践的な協調コマンド

### Boss役の調整コマンド例
```bash
# Frontend開発者への指示
echo "Backend開発者からのAPI仕様を確認して、実装を進めてください。
詳細は shared/responses/backend_to_frontend_001.md を参照。" > shared/instructions/to_frontend.md

# Backend開発者への指示  
echo "Frontend開発者からの質問に回答してください。
質問内容は shared/requests/frontend_to_backend_001.md を確認。" > shared/instructions/to_backend.md
```

### 開発者間の状況共有
```bash
# 進捗報告用ファイル
echo "## Frontend進捗
- ログインページ: 完了
- ダッシュボード: 実装中
- API連携: Backend仕様待ち

## 次のタスク
Backend仕様確定後、API連携実装開始" > shared/status/frontend_status.md
```

## 5. 協調のベストプラクティス

### 1. 明確な責任分界
- **API設計**: Backend主導、Frontend確認
- **UI/UX**: Frontend主導、PM確認
- **統合**: Fullstack主導、全員協力

### 2. 定期的な同期
```bash
# 日次ミーティング風の更新
echo "$(date): 全員の進捗を shared/status/ で確認
明日の予定を shared/plans/ で共有" > shared/daily_sync.md
```

### 3. 依存関係の管理
```markdown
# shared/dependencies/task_dependencies.md

## 依存関係マップ
Frontend UI → Backend API仕様
Backend API → Database設計
統合テスト → Frontend + Backend完成
デプロイ → 統合テスト完了
```

### 4. 問題解決の連携
```bash
# 問題報告テンプレート
echo "## 問題: CORS エラー
**発生箇所**: Frontend → Backend API呼び出し時
**エラー内容**: Access to XMLHttpRequest blocked
**対応依頼**: Backend開発者にCORS設定確認をお願いします
**緊急度**: 高（開発ブロッカー）" > shared/issues/cors_error.md
```

## 6. 効率的な対話のコツ

### 短時間での情報共有
- ファイル名に番号を付けて順序を明確に
- 緊急度（高・中・低）を明記
- 具体的な期待値・締切を記載

### 技術的な詳細の共有
- コードスニペットを含める
- 実行環境・条件を明記
- 期待する動作と実際の動作を対比

これらの方法で、各Claude Code開発者が効率的に協調できます！