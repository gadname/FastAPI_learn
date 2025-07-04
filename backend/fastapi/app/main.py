from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from mangum import Mangum

from app.db.database import Base, engine
from app.api.v1 import v1_router
from app.models.user import User  # noqa: F401. Import for table creation

app = FastAPI()


# アプリケーション起動時にテーブルを作成
@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


# ルートパスのエンドポイントを追加 - Kanbanボードを表示
@app.get("/")
async def root():
    return FileResponse("static/index.html")


allowed_origins: list[str] = [
    "http://localhost:3000",
]

app.include_router(router=v1_router, prefix="/api/v1")

# 静的ファイルのマウント
app.mount("/static", StaticFiles(directory="static"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Lambda で呼び出すASGIアプリのエントリポイント
handler = Mangum(app)
