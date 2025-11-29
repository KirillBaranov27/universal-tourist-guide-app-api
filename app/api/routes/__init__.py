from app.api.routes.auth import router as auth_router
from app.api.routes.landmarks import router as landmarks_router
from app.api.routes.favorites import router as favorites_router
from app.api.routes.reviews import router as reviews_router

__all__ = ["auth_router", "landmarks_router", "favorites_router", "reviews_router"]