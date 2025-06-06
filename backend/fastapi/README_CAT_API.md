# 猫管理API

このAPIは、`bot.py`と同じ実装パターンに従って作成された猫の情報を管理するためのAPIです。

## 実装ファイル

1. **モデル** (`app/models/cat.py`)
   - SQLAlchemyモデル定義
   - UUID型のプライマリキーを使用
   - 作成日時と更新日時を自動管理

2. **スキーマ** (`app/schemas/cat.py`)
   - `CatCreate`: 猫作成用のリクエストスキーマ
   - `CatResponse`: 猫情報のレスポンススキーマ
   - `CatAllResponse`: 全猫一覧のレスポンススキーマ
   - `UpdateCatRequest`: 猫更新用のリクエストスキーマ
   - `UpdateCatResponse`: 猫更新のレスポンススキーマ
   - `DeleteCatResponse`: 猫削除のレスポンススキーマ

3. **サービス** (`app/services/cat.py`)
   - `CatService`: ビジネスロジックを実装
   - 非同期処理（async/await）を使用
   - 適切なエラーハンドリングとロギング

4. **APIエンドポイント** (`app/api/v1/cat.py`)
   - `POST /cat/`: 新しい猫を作成
   - `GET /cat/`: 全ての猫を取得
   - `GET /cat/{cat_id}`: 特定の猫を取得
   - `PUT /cat/{cat_id}`: 猫の情報を更新
   - `DELETE /cat/{cat_id}`: 猫を削除

5. **データベースマイグレーション** (`app/db/migrations/versions/002_create_cats_table.py`)
   - catsテーブルの作成

## 使用例

### 猫を作成
```bash
curl -X POST "http://localhost:8000/api/v1/cat/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "タマ",
    "breed": "雑種",
    "age": 3,
    "weight": 4.5
  }'
```

### 全ての猫を取得
```bash
curl "http://localhost:8000/api/v1/cat/"
```

### 特定の猫を取得
```bash
curl "http://localhost:8000/api/v1/cat/{cat_id}"
```

### 猫の情報を更新
```bash
curl -X PUT "http://localhost:8000/api/v1/cat/{cat_id}" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "タマちゃん",
    "age": 4
  }'
```

### 猫を削除
```bash
curl -X DELETE "http://localhost:8000/api/v1/cat/{cat_id}"
```

## 特徴

- 非同期処理によるパフォーマンスの向上
- 適切なエラーハンドリング（404、500エラー）
- 構造化されたロギング
- Pydanticによる型安全性
- サービスレイヤーパターンによるビジネスロジックの分離