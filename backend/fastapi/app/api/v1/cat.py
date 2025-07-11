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

# Create router using base CRUD router
crud_router = BaseCRUDRouter(
    prefix="/cat",
    tags=["cat"],
    service=CatService,
    create_schema=CatCreate,
    response_schema=CatResponse,
    update_schema=UpdateCatRequest,
    all_response_schema=CatAllResponse,
    delete_response_schema=DeleteCatResponse,
    resource_name="猫"
)

# Export the router
router = crud_router.router