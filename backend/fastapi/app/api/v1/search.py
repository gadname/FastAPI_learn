from app.schemas.search import SearchResponse
from app.services.web_search import WebSearchService
from app.utils.logging import logger
from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/search", tags=["search"])


@router.get("/", response_model=SearchResponse)
async def search(q: str) -> SearchResponse:
    try:
        return await WebSearchService.search(q)
    except Exception as e:
        logger.error(f"検索APIエラー: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
