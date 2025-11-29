import sys
import os

# Добавляем корневую директорию в путь для импортов
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.database import SessionLocal
from app.models.landmark import Landmark


def seed_landmarks():
    """Заполнение базы данных достопримечательностями Санкт-Петербурга"""
    db = SessionLocal()
    
    try:
        # Удаляем существующие данные для чистоты
        db.query(Landmark).delete()
        db.commit()
        print("✅ Старые данные удалены")

        landmarks_data = [
            {
                "name": "Эрмитаж",
                "description": "Крупнейший в России и один из крупнейших в мире художественных и культурно-исторических музеев.",
                "city": "Санкт-Петербург",
                "country": "Россия",  # Теперь это поле есть в модели
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
            },
            {
                "name": "Петропавловская крепость",
                "description": "Крепость в Санкт-Петербурге, историческое ядро города.",
                "city": "Санкт-Петербург",
                "country": "Россия",
                "category": "Крепость",
                "latitude": 59.9500,
                "longitude": 30.3167,
                "address": "Петропавловская крепость, 3, Санкт-Петербург",
                "image_url": "https://example.com/images/petropavlovsk.jpg"
            },
            {
                "name": "Спас на Крови",
                "description": "Православный мемориальный храм во имя Воскресения Христова.",
                "city": "Санкт-Петербург",
                "country": "Россия",
                "category": "Храм",
                "latitude": 59.9400,
                "longitude": 30.3287,
                "address": "наб. канала Грибоедова, 2Б, Санкт-Петербург",
                "image_url": "https://example.com/images/saviour.jpg"
            }
        ]

        for landmark_data in landmarks_data:
            landmark = Landmark(**landmark_data)
            db.add(landmark)

        db.commit()
        print(f"✅ Успешно добавлено {len(landmarks_data)} достопримечательностей Санкт-Петербурга")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Ошибка при добавлении данных: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    seed_landmarks()

    