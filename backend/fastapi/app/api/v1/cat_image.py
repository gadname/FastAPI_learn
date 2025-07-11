from fastapi import APIRouter, Depends
from app.schemas.cat_image import CatImageResponse
from app.services.cat_image import CatImageService

router = APIRouter(prefix="/cat-images", tags=["cat-images"])


def get_cat_image_service():
    return CatImageService()


@router.get("/", response_model=CatImageResponse, summary="ランダムな猫画像を取得")
async def get_cat_image(
    cat_image_service: CatImageService = Depends(get_cat_image_service),
):
    """
    外部APIからランダムな猫画像のURLを取得します。

    Args:
        cat_image_service: 猫画像サービスのインスタンス

    Returns:
        CatImageResponse: 猫画像のURL

    Raises:
        HTTPException: 画像の取得に失敗した場合
    """
    image_url = await cat_image_service.get_cat_image_url()
    return CatImageResponse(url=image_url)
