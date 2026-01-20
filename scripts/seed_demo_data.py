import sys
import os
import random
from datetime import datetime, timedelta

# Добавляем корневую директорию в путь для импортов
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.database import SessionLocal
from app.models.user import User
from app.models.landmark import Landmark
from app.models.favorite import Favorite
from app.models.review import Review
from app.core.security import get_password_hash


def seed_demo_data():
    """Заполнение базы данных демонстрационными данными"""
    db = SessionLocal()
    
    try:
        print("🎬 Начало заполнения базы демо-данными...")
        
        # 1. СОЗДАЕМ ПОЛЬЗОВАТЕЛЕЙ
        print("👥 Создание пользователей...")
        users_data = [
            {
                "email": "alex@example.com",
                "password": "password123",
                "full_name": "Александр Петров"
            },
            {
                "email": "maria@example.com", 
                "password": "password123",
                "full_name": "Мария Сидорова"
            },
            {
                "email": "demo@example.com",
                "password": "demo123",
                "full_name": "Демо Пользователь"
            },
            {
                "email": "admin@example.com",
                "password": "admin123",
                "full_name": "Администратор Системы"
            }
        ]
        
        created_users = {}
        for user_data in users_data:
            existing_user = db.query(User).filter(User.email == user_data["email"]).first()
            if not existing_user:
                hashed_password = get_password_hash(user_data["password"])
                user = User(
                    email=user_data["email"],
                    hashed_password=hashed_password,
                    full_name=user_data["full_name"]
                )
                db.add(user)
                db.flush()  # Чтобы получить ID
                created_users[user_data["email"]] = user
                print(f"   ✅ Создан пользователь: {user_data['email']}")
            else:
                created_users[user_data["email"]] = existing_user
                print(f"   ⏩ Пользователь уже существует: {user_data['email']}")
        
        db.commit()
        
        # 2. СОЗДАЕМ ДОСТОПРИМЕЧАТЕЛЬНОСТИ
        print("\n🏛️ Создание достопримечательностей Санкт-Петербурга...")
        landmarks_data = [
            {
                "name": "Эрмитаж",
                "description": "Крупнейший в России и один из крупнейших в мире художественных и культурно-исторических музеев. Основан в 1764 году.",
                "city": "Санкт-Петербург",
                "country": "Россия",
                "category": "Музей",
                "latitude": 59.9398,
                "longitude": 30.3146,
                "address": "Дворцовая пл., 2",
                "image_url": "https://example.com/images/hermitage.jpg"
            },
            {
                "name": "Петергоф",
                "description": "Дворцово-парковый ансамбль на южном берегу Финского залива. Известен своими фонтанами и дворцами.",
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
                "description": "Крупнейший православный храм Санкт-Петербурга. Высота собора 101,5 метр.",
                "city": "Санкт-Петербург",
                "country": "Россия",
                "category": "Храм",
                "latitude": 59.9341,
                "longitude": 30.3061,
                "address": "Исаакиевская пл., 4",
                "image_url": "https://example.com/images/isaac.jpg"
            },
            {
                "name": "Петропавловская крепость",
                "description": "Крепость в Санкт-Петербурге, историческое ядро города. Основана 27 мая 1703 года.",
                "city": "Санкт-Петербург",
                "country": "Россия",
                "category": "Крепость", 
                "latitude": 59.9500,
                "longitude": 30.3167,
                "address": "Петропавловская крепость, 3",
                "image_url": "https://example.com/images/petropavlovsk.jpg"
            },
            {
                "name": "Спас на Крови",
                "description": "Православный мемориальный храм во имя Воскресения Христова. Построен на месте убийства Александра II.",
                "city": "Санкт-Петербург",
                "country": "Россия",
                "category": "Храм",
                "latitude": 59.9400,
                "longitude": 30.3287,
                "address": "наб. канала Грибоедова, 2Б",
                "image_url": "https://example.com/images/saviour.jpg"
            },
            {
                "name": "Кунсткамера",
                "description": "Первый музей России, учреждённый императором Петром Великим. Открыт в 1714 году.",
                "city": "Санкт-Петербург",
                "country": "Россия",
                "category": "Музей",
                "latitude": 59.9414,
                "longitude": 30.3042,
                "address": "Университетская наб., 3",
                "image_url": "https://example.com/images/kunstkamera.jpg"
            },
            {
                "name": "Летний сад",
                "description": "Парковый ансамбль, памятник садово-паркового искусства первой трети XVIII века.",
                "city": "Санкт-Петербург",
                "country": "Россия",
                "category": "Парк",
                "latitude": 59.9447,
                "longitude": 30.3358,
                "address": "Летний сад",
                "image_url": "https://example.com/images/summer_garden.jpg"
            },
            {
                "name": "Русский музей",
                "description": "Крупнейший музей русского искусства в мире. Основан в 1895 году.",
                "city": "Санкт-Петербург", 
                "country": "Россия",
                "category": "Музей",
                "latitude": 59.9386,
                "longitude": 30.3322,
                "address": "Инженерная ул., 4",
                "image_url": "https://example.com/images/russian_museum.jpg"
            },
            {
                "name": "Мариинский театр",
                "description": "Один из известнейших музыкальных театров России. Основан в 1783 году.",
                "city": "Санкт-Петербург",
                "country": "Россия",
                "category": "Театр",
                "latitude": 59.9256,
                "longitude": 30.2961,
                "address": "Театральная пл., 1",
                "image_url": "https://example.com/images/mariinsky.jpg"
            },
            {
                "name": "Казанский собор",
                "description": "Кафедральный собор Санкт-Петербургской епархии Русской Православной Церкви.",
                "city": "Санкт-Петербург",
                "country": "Россия",
                "category": "Храм",
                "latitude": 59.9344,
                "longitude": 30.3247,
                "address": "Казанская пл., 2",
                "image_url": "https://example.com/images/kazan_cathedral.jpg"
            },
            {
                "name": "Юсуповский дворец",
                "description": "Дворец на Мойке, памятник истории и культуры федерального значения.",
                "city": "Санкт-Петербург",
                "country": "Россия",
                "category": "Дворец",
                "latitude": 59.9297,
                "longitude": 30.2981,
                "address": "наб. реки Мойки, 94",
                "image_url": "https://example.com/images/yusupov_palace.jpg"
            },
            {
                "name": "Невский проспект",
                "description": "Главная улица Санкт-Петербурга. Протяжённость 4,5 км.",
                "city": "Санкт-Петербург",
                "country": "Россиia",
                "category": "Архитектура",
                "latitude": 59.9343,
                "longitude": 30.3351,
                "address": "Невский проспект",
                "image_url": "https://example.com/images/nevsky.jpg"
            }
        ]
        
        created_landmarks = {}
        for landmark_data in landmarks_data:
            existing_landmark = db.query(Landmark).filter(
                Landmark.name == landmark_data["name"],
                Landmark.city == landmark_data["city"]
            ).first()
            
            if not existing_landmark:
                landmark = Landmark(**landmark_data)
                db.add(landmark)
                db.flush()
                created_landmarks[landmark_data["name"]] = landmark
                print(f"   ✅ Создана достопримечательность: {landmark_data['name']}")
            else:
                created_landmarks[landmark_data["name"]] = existing_landmark
                print(f"   ⏩ Достопримечательность уже существует: {landmark_data['name']}")
        
        db.commit()
        
        # 3. ДОБАВЛЯЕМ ИЗБРАННОЕ
        print("\n❤️ Добавление избранных достопримечательностей...")
        
        # Определяем какие достопримечательности кому нравятся
        favorites_mapping = {
            "alex@example.com": ["Эрмитаж", "Петропавловская крепость", "Кунсткамера"],
            "maria@example.com": ["Петергоф", "Спас на Крови", "Летний сад"],
            "demo@example.com": ["Исаакиевский собор", "Русский музей", "Мариинский театр"],
            "admin@example.com": ["Казанский собор", "Юсуповский дворец", "Невский проспект"]
        }
        
        favorites_count = 0
        for user_email, landmark_names in favorites_mapping.items():
            user = created_users[user_email]
            for landmark_name in landmark_names:
                landmark = created_landmarks[landmark_name]
                
                # Проверяем, не добавлено ли уже в избранное
                existing_favorite = db.query(Favorite).filter(
                    Favorite.user_id == user.id,
                    Favorite.landmark_id == landmark.id
                ).first()
                
                if not existing_favorite:
                    favorite = Favorite(user_id=user.id, landmark_id=landmark.id)
                    db.add(favorite)
                    favorites_count += 1
        
        db.commit()
        print(f"   ✅ Добавлено {favorites_count} записей в избранное")
        
        # 4. ДОБАВЛЯЕМ ОТЗЫВЫ И ОЦЕНКИ
        print("\n⭐ Добавление отзывов и оценок...")
        
        reviews_data = [
            # Отзывы для Эрмитажа
            {
                "user": "alex@example.com",
                "landmark": "Эрмитаж", 
                "rating": 5,
                "comment": "Потрясающий музей! Коллекция просто огромная, одного дня точно не хватит. Обязательно вернусь!"
            },
            {
                "user": "maria@example.com",
                "landmark": "Эрмитаж",
                "rating": 4,
                "comment": "Очень красиво, но слишком много народу. Советую приходить к открытию."
            },
            
            # Отзывы для Петергофа
            {
                "user": "maria@example.com", 
                "landmark": "Петергоф",
                "rating": 5,
                "comment": "Фонтаны просто волшебные! Особенно впечатлил Большой каскад. Обязательно к посещению!"
            },
            {
                "user": "demo@example.com",
                "landmark": "Петергоф", 
                "rating": 5,
                "comment": "Прекрасное место для прогулки. Парк ухоженный, фонтаны работают отлично."
            },
            
            # Отзывы для Исаакиевского собора
            {
                "user": "demo@example.com",
                "landmark": "Исаакиевский собор",
                "rating": 5, 
                "comment": "Вид с колоннады просто захватывает дух! Подъем тяжелый, но оно того стоит."
            },
            
            # Отзывы для Петропавловской крепости
            {
                "user": "alex@example.com",
                "landmark": "Петропавловская крепость", 
                "rating": 4,
                "comment": "Интересное историческое место. Понравился музей и собор."
            },
            
            # Отзывы для Спаса на Крови
            {
                "user": "maria@example.com",
                "landmark": "Спас на Крови",
                "rating": 5,
                "comment": "Невероятная мозаика! Внутри еще красивее, чем снаружи. Обязательно возьмите аудиогид."
            },
            
            # Отзывы для Кунсткамеры
            {
                "user": "alex@example.com", 
                "landmark": "Кунсткамера",
                "rating": 4,
                "comment": "Очень необычный музей. Коллекция анатомических редкостей впечатляет."
            },
            
            # Отзывы для Русского музея
            {
                "user": "demo@example.com",
                "landmark": "Русский музей",
                "rating": 5,
                "comment": "Прекрасная коллекция русского искусства. Особенно понравились залы с иконами и авангардом."
            },
            
            # Отзывы для Мариинского театра
            {
                "user": "admin@example.com",
                "landmark": "Мариинский театр", 
                "rating": 5,
                "comment": "Великолепная акустика и потрясающие постановки. Настоящая жемчужина Петербурга!"
            }
        ]
        
        reviews_count = 0
        for review_data in reviews_data:
            user = created_users[review_data["user"]]
            landmark = created_landmarks[review_data["landmark"]]
            
            # Проверяем, не оставил ли пользователь уже отзыв
            existing_review = db.query(Review).filter(
                Review.user_id == user.id,
                Review.landmark_id == landmark.id
            ).first()
            
            if not existing_review:
                review = Review(
                    user_id=user.id,
                    landmark_id=landmark.id,
                    rating=review_data["rating"],
                    comment=review_data["comment"]
                )
                db.add(review)
                reviews_count += 1
        
        db.commit()
        print(f"   ✅ Добавлено {reviews_count} отзывов")
        
        # 5. ВЫВОДИМ СВОДКУ
        print("\n📊 Сводка по созданным данным:")
        print(f"   👥 Пользователей: {len(created_users)}")
        print(f"   🏛️ Достопримечательностей: {len(created_landmarks)}")
        print(f"   ❤️ Записей в избранном: {favorites_count}")
        print(f"   ⭐ Отзывов: {reviews_count}")
        
        print("\n🎉 Демо-данные успешно созданы!")
        print("\n🔑 Данные для входа:")
        print("   📧 alex@example.com / password: password123")
        print("   📧 maria@example.com / password: password123") 
        print("   📧 demo@example.com / password: demo123")
        print("   📧 admin@example.com / password: admin123")
        
        print("\n🌐 Для тестирования откройте: http://127.0.0.1:8000/docs")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Ошибка при создании демо-данных: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_demo_data()