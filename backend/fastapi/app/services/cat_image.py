import httpx
from fastapi import HTTPException

THE_CAT_API_URL = "https://api.thecatapi.com/v1/images/search"

class CatImageService:
    async def get_cat_image_url(self) -> str:
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(THE_CAT_API_URL)
                response.raise_for_status()  # Raise an exception for bad status codes
                data = response.json()
                if data and isinstance(data, list) and data[0].get("url"):
                    return data[0]["url"]
                else:
                    # Log an error or handle unexpected response structure
                    raise HTTPException(status_code=500, detail="Unexpected response from TheCatAPI")
            except httpx.HTTPStatusError as e:
                # Log the error e
                raise HTTPException(status_code=500, detail=f"Error fetching cat image from TheCatAPI: {e.response.status_code}")
            except httpx.RequestError as e:
                # Log the error e
                raise HTTPException(status_code=500, detail=f"Request error while fetching cat image: {e}")
            except Exception as e:
                # Log the error e
                raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")
