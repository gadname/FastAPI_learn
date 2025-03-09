from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum

from app.routers import bot_create
from app.db.database import Base, engine

app = FastAPI()

# アプリケーション起動時にテーブルを作成


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

allowed_origins: list[str] = [
    "http://localhost:3000",
]

app.include_router(router=bot_create.router, prefix="/api/v1")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Lambda で呼び出すASGIアプリのエントリポイント
handler = Mangum(app)
