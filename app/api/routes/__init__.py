from app.api.routes.auth import router as auth_router
from app.api.routes.landmarks import router as landmarks_router
from app.api.routes.favorites import router as favorites_router
from app.api.routes.reviews import router as reviews_router
from app.api.routes.profile import router as profile_router
from app.api.routes.discussions import router as discussions_router
from app.api.routes.cities import router as cities_router
from app.api.routes.notifications import router as notifications_router

# Импортируем схемы, которые теперь существуют
from app.schemas.city import CityBase, CityProfileResponse, CityFilters, CityStatsResponse

__all__ = [
    "auth_router", 
    "landmarks_router", 
    "favorites_router", 
    "reviews_router",
    "profile_router",
    "discussions_router",
    "cities_router",
    "notifications_router",
    "CityBase", 
    "CityProfileResponse", 
    "CityFilters", 
    "CityStatsResponse",
]