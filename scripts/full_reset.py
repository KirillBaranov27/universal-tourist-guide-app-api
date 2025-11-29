import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.database import engine, Base
from app.models.user import User
from app.models.landmark import Landmark
from app.core.security import get_password_hash

def full_reset():
    """Полный сброс и пересоздание базы с тестовыми данными"""
    print("🔄 Полный сброс базы данных...")
    
    # Удаляем все таблицы
    Base.metadata.drop_all(bind=engine)
    print("✅ Таблицы удалены")
    
    # Создаем таблицы заново
    Base.metadata.create_all(bind=engine)
    print("✅ Таблицы созданы заново")
    
    # Создаем тестового пользователя
    from app.core.database import SessionLocal
    db = SessionLocal()
    
    try:
        # Создаем пользователя
        hashed_password = get_password_hash("testpassword123")
        user = User(
            email="test@example.com",
            hashed_password=hashed_password,
            full_name="Test User"
        )
        db.add(user)
        
        # Создаем достопримечательности СПб
        landmarks_data = [
            {
                "name": "Эрмитаж",
                "description": "Крупнейший в России и один из крупнейших в мире художественных и культурно-исторических музеев.",
                "city": "Санкт-Петербург",
                "country": "Россия",
                "category": "Музей",
                "latitude": 59.9398,
                "longitude": 30.3146,
                "address": "Дворцовая пл., 2, Санкт-Петербург",
                "image_url": "https://example.com/images/hermitage.jpg"
            },
            {
                "name": "Петергоф",
                "description": "Дворцово-парковый ансамбль на южном берегу Финского залива, известный своими фонтанами.",
                "city": "Санкт-Петербург", 
                "country": "Россия",
                "category": "Дворец",
                "latitude": 59.8833,
                "longitude": 29.9000,
                "address": "Разводная ул., 2, Петергоф",
                "image_url": "https://example.com/images/peterhof.jpg"
            },
            {
                "name": "Исаакиевский собор",
                "description": "Крупнейший православный храм Санкт-Петербурга, музей-памятник.",
                "city": "Санкт-Петербург",
                "country": "Россия",
                "category": "Храм",
                "latitude": 59.9341,
                "longitude": 30.3061,
                "address": "Исаакиевская пл., 4, Санкт-Петербург",
                "image_url": "https://example.com/images/isaac.jpg"
            }
        ]
        
        for landmark_data in landmarks_data:
            landmark = Landmark(**landmark_data)
            db.add(landmark)
        
        db.commit()
        print("✅ Тестовый пользователь создан: test@example.com / testpassword123")
        print(f"✅ Добавлено {len(landmarks_data)} достопримечательностей СПб")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Ошибка: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    full_reset()