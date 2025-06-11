from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum

# Update imports from app.db.database
from app.db.database import Base, async_engine, engine_sync # Import both engines

from app.api.v1 import v1_router

app = FastAPI()


# アプリケーション起動時にテーブルを作成
@app.on_event("startup")
async def startup():
    # For async engine
    async with async_engine.begin() as conn:
        # This creates all tables defined on Base metadata for the async connection.
        await conn.run_sync(Base.metadata.create_all)

    # For sync engine (explicitly create tables for sync operations)
    # This ensures tables are recognized by the sync components.
    # Base.metadata.create_all is a synchronous call.
    with engine_sync.connect() as conn: # Use a connection from the sync engine
        Base.metadata.create_all(bind=engine_sync) # Pass engine_sync to create_all
        conn.commit() # Commit the table creation DDL, important for some DBs


# ルートパスのエンドポイントを追加
@app.get("/")
async def root():
    return {"message": "Welcome to FastAPI Application"}


allowed_origins: list[str] = [
    "http://localhost:3000",
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
