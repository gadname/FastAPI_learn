# 猫管理APIの実装

## 概要
FastAPIアプリケーションに猫の情報を管理するためのAPIを追加しました。
既存の`bot.py`と同じアーキテクチャパターンに従って実装しています。

## 変更内容

### 新規追加ファイル
- `app/models/cat.py` - 猫のデータベースモデル
- `app/schemas/cat.py` - Pydanticスキーマ（リクエスト/レスポンス）
- `app/services/cat.py` - ビジネスロジックを含むサービスレイヤー
- `app/api/v1/cat.py` - APIエンドポイント定義
- `app/db/migrations/versions/002_create_cats_table.py` - データベースマイグレーション
- `README_CAT_API.md` - API実装の詳細ドキュメント

### 更新ファイル
- `app/api/v1/__init__.py` - 猫ルーターをv1 APIに追加

## 実装の特徴

- **非同期処理**: `async/await`による高パフォーマンス実装
- **エラーハンドリング**: 適切なHTTPステータスコードとエラーメッセージ
- **ロギング**: 構造化されたログ出力
- **型安全性**: Pydanticによる型検証
- **サービスレイヤーパターン**: ビジネスロジックの分離

## APIエンドポイント

| メソッド | エンドポイント | 説明 |
|---------|---------------|------|
| POST | `/api/v1/cat/` | 新しい猫を作成 |
| GET | `/api/v1/cat/` | 全ての猫を取得 |
| GET | `/api/v1/cat/{cat_id}` | 特定の猫を取得 |
| PUT | `/api/v1/cat/{cat_id}` | 猫の情報を更新 |
| DELETE | `/api/v1/cat/{cat_id}` | 猫を削除 |

## テスト方法

```bash
# 猫を作成
curl -X POST "http://localhost:8000/api/v1/cat/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "タマ",
    "breed": "雑種",
    "age": 3,
    "weight": 4.5
  }'

# 全ての猫を取得
curl "http://localhost:8000/api/v1/cat/"
```

## チェックリスト

- [x] コードはプロジェクトの規約に従っている
- [x] 非同期処理を使用している
- [x] エラーハンドリングが適切に実装されている
- [x] ログ出力が実装されている
- [x] Pydanticスキーマで型検証を行っている
- [x] サービスレイヤーパターンを使用している
- [x] マイグレーションファイルを作成している
- [x] ドキュメントを作成している