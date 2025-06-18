from fastapi import APIRouter

router = APIRouter(prefix="/hello", tags=["hello"])

@router.get("/", summary="Greeting endpoint")
async def hello() -> dict[str, str]:
    """
    A simple endpoint that returns a greeting message.
    """
    return {"message": "Hello, FastAPI!"}
