from fastapi import APIRouter, Depends
from app.schemas.cat_image import CatImageResponse
from app.services.cat_image import CatImageService

router = APIRouter()

def get_cat_image_service():
    return CatImageService()

@router.get("/cat/image", response_model=CatImageResponse)
async def get_cat_image(
    cat_image_service: CatImageService = Depends(get_cat_image_service)
):
    image_url = await cat_image_service.get_cat_image_url()
    return CatImageResponse(url=image_url)
