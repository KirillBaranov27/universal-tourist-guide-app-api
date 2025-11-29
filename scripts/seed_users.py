import sys
import os

# Добавляем корневую директорию в путь для импортов
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.database import SessionLocal
from app.models.user import User
from app.core.security import get_password_hash

def seed_users():
    """Создание тестового пользователя"""
    db = SessionLocal()
    
    try:
        # Проверяем, существует ли пользователь
        existing_user = db.query(User).filter(User.email == "test@example.com").first()
        if existing_user:
            print("✅ Пользователь test@example.com уже существует")
            return

        # Создаем тестового пользователя
        hashed_password = get_password_hash("testpassword123")
        user = User(
            email="test@example.com",
            hashed_password=hashed_password,
            full_name="Test User"
        )
        
        db.add(user)
        db.commit()
        print("✅ Пользователь test@example.com успешно создан")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Ошибка при создании пользователя: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_users()