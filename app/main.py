from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings

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
    """Корневой эндпоинт для проверки работы API"""
    return {
        "message": "Universal Tourist Guide API", 
        "status": "работает",
        "version": "0.1.0"
    }

@app.get("/health")
async def health_check():
    """Эндпоинт для проверки здоровья приложения"""
    return {"status": "healthy"}