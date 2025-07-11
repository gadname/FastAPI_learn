from app.api.base.base_router import BaseCRUDRouter
from app.schemas.cat import (
    CatCreate,
    CatResponse,
    CatAllResponse,
    UpdateCatResponse,
    UpdateCatRequest,
    DeleteCatResponse,
)
from app.services.cat import CatService
from app.models.cat import Cat


# Create CRUD router instance using the base class
cat_router = BaseCRUDRouter(
    prefix="/cat",
    tags=["cat"],
    service_class=CatService,
    response_model=CatResponse,
    all_response_model=CatAllResponse,
    update_response_model=UpdateCatResponse,
    delete_response_model=DeleteCatResponse,
    resource_name="cat",
    resource_name_ja="猫",
    use_legacy_adapter=True,
)

# Export the router
router = cat_router.get_router()