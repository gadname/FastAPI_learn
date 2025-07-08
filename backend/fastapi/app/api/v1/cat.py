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

# Create the router using the base CRUD router
cat_router = BaseCRUDRouter[
    CatCreate,
    CatResponse,
    CatAllResponse,
    UpdateCatRequest,
    UpdateCatResponse,
    DeleteCatResponse
](
    prefix="/cat",
    tags=["cat"],
    service_class=CatService,
    create_schema=CatCreate,
    response_schema=CatResponse,
    all_response_schema=CatAllResponse,
    update_request_schema=UpdateCatRequest,
    update_response_schema=UpdateCatResponse,
    delete_response_schema=DeleteCatResponse,
    entity_name="猫"
)

# Export the router
router = cat_router.router