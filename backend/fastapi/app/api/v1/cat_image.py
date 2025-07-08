from fastapi import Depends
from app.api.base.base_router import BaseRouter
from app.schemas.cat_image import CatImageResponse
from app.services.cat_image import CatImageService
from app.api.dependencies.common import get_cat_image_service_dependency


class CatImageRouter(BaseRouter):
    """Cat image router using base router pattern"""
    
    def _setup_routes(self):
        @self.router.get("/", response_model=CatImageResponse)
        async def get_cat_image(
            cat_image_service: CatImageService = Depends(get_cat_image_service_dependency),
        ):
            image_url = await cat_image_service.get_cat_image_url()
            return CatImageResponse(url=image_url)


# Create the router instance
cat_image_router = CatImageRouter(prefix="/cat-images", tags=["cat-images"])

# Export the router
router = cat_image_router.router
