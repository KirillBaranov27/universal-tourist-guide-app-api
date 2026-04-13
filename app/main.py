from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Импорты роутеров
from app.api.routes.auth import router as auth_router
from app.api.routes.landmarks import router as landmarks_router
from app.api.routes.favorites import router as favorites_router
from app.api.routes.reviews import router as reviews_router
from app.api.routes.profile import router as profile_router
from app.api.routes.discussions import router as discussions_router
from app.api.routes.cities import router as cities_router

# Проверяем наличие роутеров
try:
    from app.api.routes import router as users_router
    HAS_USERS_ROUTER = True
except ImportError:
    HAS_USERS_ROUTER = False

try:
<<<<<<< Updated upstream
    # Явно импортируем модели для регистрации
    from app.models.user import User
    from app.models.landmark import Landmark
    from app.models.favorite import Favorite
    from app.models.review import Review
    from app.models.discussion import Discussion, DiscussionAnswer
    from app.models.city import CityProfile, CityCategoryStats
    from app.models.notification import Notification
    
    # Создаём таблицы
    Base.metadata.create_all(bind=engine)
    print("✅ Таблицы успешно созданы!")
    
except Exception as e:
    print(f"❌ Ошибка при создании таблиц: {e}")
=======
    from app.api.routes.notifications import router as notifications_router
    HAS_NOTIFICATIONS_ROUTER = True
except ImportError:
    HAS_NOTIFICATIONS_ROUTER = False
>>>>>>> Stashed changes

app = FastAPI(
    title="Universal Tourist Guide API",
    version="0.7.0",
    description="Бэкенд API для мобильного приложения-гида по достопримечательностям",
<<<<<<< Updated upstream
    version = "0.8.0",  # Обновляем версию
=======
    openapi_url="/openapi.json",
>>>>>>> Stashed changes
    docs_url="/docs",
    redoc_url="/redoc",
)

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # В продакшене укажите конкретные домены
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключаем роутеры
<<<<<<< Updated upstream
from app.api.routes import auth, landmarks, favorites, reviews, profile, discussions, notifications
app.include_router(auth.router, prefix="/api/auth", tags=["Аутентификация"])
app.include_router(landmarks.router, prefix="/api", tags=["Достопримечательности"])
app.include_router(favorites.router, prefix="/api", tags=["Избранное"])
app.include_router(reviews.router, prefix="/api", tags=["Отзывы и оценки"])
app.include_router(profile.router, prefix="/api", tags=["Профили пользователей"])
app.include_router(discussions.router, prefix="/api", tags=["Обсуждения"])
app.include_router(cities.router, prefix="/api", tags=["Города"])
app.include_router(notifications.router, prefix="/api", tags=["Уведомления"])
=======
app.include_router(auth_router, prefix="/api/auth", tags=["Аутентификация"])
app.include_router(landmarks_router, prefix="/api/landmarks", tags=["Достопримечательности"])
app.include_router(favorites_router, prefix="/api/favorites", tags=["Избранное"])
app.include_router(reviews_router, prefix="/api/reviews", tags=["Отзывы и оценки"])
app.include_router(profile_router, prefix="/api/profile", tags=["Профили пользователей"])
app.include_router(discussions_router, prefix="/api/discussions", tags=["Обсуждения"])
app.include_router(cities_router, prefix="/api/cities", tags=["Города"])
>>>>>>> Stashed changes

# Подключаем users_router, если он существует
if HAS_USERS_ROUTER:
    app.include_router(users_router, prefix="/api/users", tags=["Пользователи"])

# Подключаем notifications_router, если он существует
if HAS_NOTIFICATIONS_ROUTER:
    app.include_router(notifications_router, prefix="/api/notifications", tags=["Уведомления"])

# Корневой эндпоинт
@app.get("/")
async def root():
    return {
<<<<<<< Updated upstream
        "message": "Universal Tourist Guide API", 
        "status": "работает",
        "version": "0.8.0",  # Обновляем версию
        "database": "PostgreSQL",
        "features": [
            "аутентификация пользователей",
            "CRUD операции для достопримечательностей", 
            "поиск и фильтрация",
            "геолокационный поиск",
            "система избранного",
            "система оценок и отзывов",
            "профили пользователей с репутацией",
            "форум обсуждений",
            "профили городов с фильтрацией",
            "система уведомлений"  # Добавляем новую фичу
        ]
=======
        "message": "Universal Tourist Guide API",
        "version": "0.7.0",
        "docs": "/docs",
        "openapi": "/openapi.json"
>>>>>>> Stashed changes
    }

# Эндпоинт для проверки здоровья
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Эндпоинт для получения информации о API
@app.get("/api/info")
async def api_info():
    return {
<<<<<<< Updated upstream
        "status": "operational",
        "version": "0.8.0",  # Обновляем версию
        "database": "connected",
        "features": {
            "authentication": True,
            "landmarks_crud": True,
            "search_filters": True,
            "geolocation": True,
            "pagination": True,
            "favorites": True,
            "reviews": True,
            "ratings": True,
            "user_profiles": True,
            "discussions": True,
            "city_profiles": True,
            "notifications": True  # Добавляем новую фичу
=======
        "name": "Universal Tourist Guide API",
        "version": "0.7.0",
        "description": "Бэкенд для мобильного приложения-гида по достопримечательностям",
        "author": "Tourist Guide Team",
        "endpoints": {
            "auth": "/api/auth",
            "landmarks": "/api/landmarks",
            "favorites": "/api/favorites",
            "reviews": "/api/reviews",
            "profile": "/api/profile",
            "discussions": "/api/discussions",
            "cities": "/api/cities",
>>>>>>> Stashed changes
        }
    }

# Обработчик для 404 ошибок
@app.exception_handler(404)
async def not_found_handler(request, exc):
    return {
        "detail": "Эндпоинт не найден",
        "available_endpoints": [
            "/api/auth",
            "/api/landmarks",
            "/api/favorites",
            "/api/reviews",
            "/api/profile",
            "/api/discussions",
            "/api/cities",
            "/docs",
            "/openapi.json"
        ]
    }

# Если есть эндпоинт для фильтров
@app.get("/api/filters/all")
async def get_all_filters():
    """Эндпоинт для получения всех фильтров"""
    # Этот эндпоинт может быть реализован в отдельном роутере
    # Здесь заглушка для совместимости с документацией
    return {
        "cities": [],
        "categories": []
    }

# Эндпоинт для проверки версии
@app.get("/api/version")
async def get_version():
    return {"version": "0.7.0"}

# Эндпоинт для получения метрик (можно использовать для мониторинга)
@app.get("/api/metrics")
async def get_metrics():
    return {
        "status": "ok",
        "timestamp": "2026-01-20T10:00:00Z",
        "uptime": "не реализовано"
    }

# Запуск приложения (для локальной разработки)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)