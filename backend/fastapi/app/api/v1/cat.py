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
from app.services.base.base_service import LegacyServiceAdapter

# Create a router instance using the base CRUD router
cat_router = BaseCRUDRouter(
    prefix="/cat",
    tags=["cat"],
    service_class=LegacyServiceAdapter(CatService),
    create_schema=CatCreate,
    response_schema=CatResponse,
    all_response_schema=CatAllResponse,
    update_request_schema=UpdateCatRequest,
    update_response_schema=UpdateCatResponse,
    delete_response_schema=DeleteCatResponse,
    entity_name="cat",
    entity_name_jp="猫",
)

# Export the router
router = cat_router.router