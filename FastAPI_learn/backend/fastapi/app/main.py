from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.endpoints import cats
from app.db.session import engine
from app.db.base_class import Base

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Cat Management API",
    description="API for managing cat information",
    version="1.0.0"
)

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(
    cats.router,
    prefix="/api/v1",
    tags=["cats"]
)

@app.get("/")
def read_root():
    return {"message": "Welcome to Cat Management API"}