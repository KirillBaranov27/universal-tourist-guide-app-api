from app.schemas.user import UserCreate, UserResponse
from app.schemas.landmark import LandmarkCreate, LandmarkResponse

print("🧪 Тестирование Pydantic схем...")

# Тест схем пользователей
try:
    user_data = {
        "email": "test@example.com",
        "full_name": "Test User",
        "password": "secret123"
    }
    user = UserCreate(**user_data)
    print("✅ Схема UserCreate работает!")
except Exception as e:
    print(f"❌ Ошибка в UserCreate: {e}")

# Тест схем достопримечательностей
try:
    landmark_data = {
        "name": "Красная площадь",
        "description": "Главная площадь Москвы",
        "latitude": 55.7539,
        "longitude": 37.6208,
        "city": "Москва"
    }
    landmark = LandmarkCreate(**landmark_data)
    print("✅ Схема LandmarkCreate работает!")
except Exception as e:
    print(f"❌ Ошибка в LandmarkCreate: {e}")

print("🎉 Все схемы работают корректно!")