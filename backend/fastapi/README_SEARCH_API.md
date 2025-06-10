# Web検索API

DuckDuckGoの検索結果を取得する簡易APIです。`/api/v1/search/` エンドポイントから利用できます。

## 実装ファイル

1. **スキーマ** (`app/schemas/search.py`)
   - `SearchResponseItem`: 検索結果1件分の情報
   - `SearchResponse`: 検索結果のリスト
2. **サービス** (`app/services/web_search.py`)
   - `WebSearchService.search`: DuckDuckGo APIを呼び出して結果を取得
3. **APIエンドポイント** (`app/api/v1/search.py`)
   - `GET /search/?q=キーワード`: 検索結果を取得

## 使用例
```bash
curl "http://localhost:8000/api/v1/search/?q=fastapi"
```
