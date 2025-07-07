import httpx
from fastapi import HTTPException

THE_CAT_API_URL = "https://api.thecatapi.com/v1/images/search"


class CatImageService:
    async def get_cat_image_url(self) -> str:
        async with httpx.AsyncClient(timeout=10.0) as client:
            try:
                response = await client.get(THE_CAT_API_URL)
                response.raise_for_status()
                data = response.json()

                # APIレスポンスの基本チェック
                if not data or not isinstance(data, list):
                    raise HTTPException(
                        status_code=503,
                        detail="External service returned unexpected response",
                    )

                # 最初の画像データにURLが含まれているかチェック
                first_image = data[0]
                if not first_image.get("url"):
                    raise HTTPException(
                        status_code=503,
                        detail="External service returned unexpected response",
                    )

                return first_image["url"]
            except httpx.HTTPStatusError:
                raise HTTPException(
                    status_code=503,
                    detail="External cat image service is temporarily unavailable",
                )
            except httpx.RequestError:
                raise HTTPException(
                    status_code=503, detail="Failed to connect to cat image service"
                )
            except Exception:
                raise HTTPException(
                    status_code=500,
                    detail="An unexpected error occurred while fetching cat image",
                )
