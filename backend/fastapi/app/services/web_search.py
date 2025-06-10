import httpx

from app.schemas.search import SearchResponse, SearchResponseItem
from app.utils.logging import logger


class WebSearchService:
    @staticmethod
    async def search(query: str) -> SearchResponse:
        url = "https://api.duckduckgo.com/"
        params = {"q": query, "format": "json", "no_redirect": 1, "no_html": 1}
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, params=params, timeout=10)
                response.raise_for_status()
                data = response.json()
        except Exception as e:
            logger.error(f"検索失敗: {str(e)}")
            raise

        results = []
        for item in data.get("RelatedTopics", []):
            # Skip nested lists
            if (
                isinstance(item, dict)
                and "Text" in item
                and "FirstURL" in item
            ):
                results.append(
                    SearchResponseItem(
                        title=item["Text"],
                        url=item["FirstURL"],
                    )
                )
            # Some items have 'Topics' list
            elif "Topics" in item:
                for sub in item.get("Topics", []):
                    if (
                        isinstance(sub, dict)
                        and "Text" in sub
                        and "FirstURL" in sub
                    ):
                        results.append(
                            SearchResponseItem(
                                title=sub["Text"],
                                url=sub["FirstURL"],
                            )
                        )
        return SearchResponse(results=results[:5])
