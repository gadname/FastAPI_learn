from app.api.base.base_router import BaseRouter


class HelloRouter(BaseRouter):
    """Hello router using base router pattern"""
    
    def _setup_routes(self):
        @self.router.get("/", summary="Greeting endpoint")
        async def hello() -> dict[str, str]:
            """
            A simple endpoint that returns a greeting message.
            """
            return {"message": "Hello, FastAPI!"}


# Create the router instance
hello_router = HelloRouter(prefix="/hello", tags=["hello"])

# Export the router
router = hello_router.router
