from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.database import engine, Base
from app.api.routes import cities

print("🔄 Создание таблиц в базе данных...")

try:
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

# Создание основного приложения FastAPI
app = FastAPI(
    title="Universal Tourist Guide API",
    description="Бэкенд API для мобильного приложения-гида по достопримечательностям",
    version = "0.8.0",  # Обновляем версию
    docs_url="/docs",
    redoc_url="/redoc"
)

# Настройка CORS для работы с мобильным приложением
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключаем роутеры
from app.api.routes import auth, landmarks, favorites, reviews, profile, discussions, notifications
app.include_router(auth.router, prefix="/api/auth", tags=["Аутентификация"])
app.include_router(landmarks.router, prefix="/api", tags=["Достопримечательности"])
app.include_router(favorites.router, prefix="/api", tags=["Избранное"])
app.include_router(reviews.router, prefix="/api", tags=["Отзывы и оценки"])
app.include_router(profile.router, prefix="/api", tags=["Профили пользователей"])
app.include_router(discussions.router, prefix="/api", tags=["Обсуждения"])
app.include_router(cities.router, prefix="/api", tags=["Города"])
app.include_router(notifications.router, prefix="/api", tags=["Уведомления"])

@app.get("/")
async def root():
    return {
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
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/api/status")
async def api_status():
    return {
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
        }
    }