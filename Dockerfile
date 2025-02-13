FROM python:3.11-slim

WORKDIR /app

# システムの依存関係をインストール
RUN apt-get update && apt-get install -y \
    curl \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Poetryのインストール
RUN curl -sSL https://install.python-poetry.org | python3 -

# PATHにPoetryを追加
ENV PATH="/root/.local/bin:$PATH"

# Poetry設定
RUN poetry config virtualenvs.create false

# 依存関係ファイルをコピー
COPY pyproject.toml poetry.lock* ./

# 依存関係のインストール
RUN poetry install --no-interaction --no-root

# アプリケーションのソースコードをコピー
COPY . .

# アプリケーションのインストール
RUN poetry install --no-interaction

# Mangumハンドラーを使用してFastAPIアプリケーションを実行
CMD ["python", "-m", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]