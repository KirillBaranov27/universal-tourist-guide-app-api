from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.database import engine, Base

print("🔄 Создание таблиц в базе данных...")

try:
    # Явно импортируем модели для регистрации
    from app.models.user import User
    from app.models.landmark import Landmark
    
    # Создаём таблицы
    Base.metadata.create_all(bind=engine)
    print("✅ Таблицы успешно созданы!")
    
except Exception as e:
    print(f"❌ Ошибка при создании таблиц: {e}")

# Создание основного приложения FastAPI
app = FastAPI(
    title="Universal Tourist Guide API",
    description="Бэкенд API для мобильного приложения-гида по достопримечательностям",
    version="0.1.0"
)

# Настройка CORS для работы с мобильным приложением
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {
        "message": "Universal Tourist Guide API", 
        "status": "работает",
        "version": "0.1.0",
        "database": "PostgreSQL"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}