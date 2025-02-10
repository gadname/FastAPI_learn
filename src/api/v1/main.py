# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum

from src.api.v1 import v1_router

app = FastAPI()

allowed_origins: list[str] = [
    "http://localhost:3000",  # ローカル開発用
    # Amplify上のURLなど
]

app.include_router(router=v1_router, prefix="/api/v1")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Lambda で呼び出すASGIアプリのエントリポイント
handler = Mangum(app)
