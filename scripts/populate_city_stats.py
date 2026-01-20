import sys
import os
from pathlib import Path

# Добавляем корневую директорию проекта в sys.path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from sqlalchemy import func, select
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.city import CityProfile, CityCategoryStats
from app.models.landmark import Landmark
from app.models.review import Review
from app.models.discussion import Discussion


def populate_city_stats_sync():
    """Заполняет таблицы статистики городов (синхронная версия)"""
    db = SessionLocal()
    try:
        # Получаем все уникальные города из достопримечательностей
        cities = db.execute(
            select(Landmark.city, Landmark.country).distinct()
        ).all()
        
        print(f"Найдено {len(cities)} городов для обработки")
        
        for city_name, country in cities:
            print(f"Обработка города: {city_name}, {country}")
            
            # Считаем статистику
            # 1. Количество достопримечательностей
            total_landmarks = db.execute(
                select(func.count()).where(Landmark.city == city_name)
            ).scalar()
            
            # 2. Количество отзывов
            total_reviews = db.execute(
                select(func.count())
                .select_from(Review)
                .join(Landmark, Review.landmark_id == Landmark.id)
                .where(Landmark.city == city_name)
            ).scalar() or 0
            
            # 3. Количество обсуждений
            total_discussions = db.execute(
                select(func.count()).where(Discussion.city == city_name)
            ).scalar() or 0
            
            # 4. Средний рейтинг
            average_rating = db.execute(
                select(func.avg(Review.rating))
                .select_from(Review)
                .join(Landmark, Review.landmark_id == Landmark.id)
                .where(Landmark.city == city_name)
            ).scalar() or 0.0
            
            # Создаем или обновляем запись
            city_profile = db.query(CityProfile).get(city_name)
            if not city_profile:
                city_profile = CityProfile(
                    city_name=city_name,
                    country=country,
                    total_landmarks=total_landmarks,
                    total_reviews=total_reviews,
                    total_discussions=total_discussions,
                    average_rating=float(average_rating)
                )
                db.add(city_profile)
                print(f"  Добавлен профиль: {total_landmarks} достопримечательностей, {total_reviews} отзывов")
            else:
                city_profile.country = country
                city_profile.total_landmarks = total_landmarks
                city_profile.total_reviews = total_reviews
                city_profile.total_discussions = total_discussions
                city_profile.average_rating = float(average_rating)
                print(f"  Обновлен профиль: {total_landmarks} достопримечательностей, {total_reviews} отзывов")
            
            # Статистика по категориям
            categories_result = db.execute(
                select(Landmark.category, func.count())
                .where(Landmark.city == city_name)
                .group_by(Landmark.category)
            ).all()
            
            for category, count in categories_result:
                category_stat = db.query(CityCategoryStats).filter(
                    CityCategoryStats.city_name == city_name,
                    CityCategoryStats.category == category
                ).first()
                
                if not category_stat:
                    category_stat = CityCategoryStats(
                        city_name=city_name,
                        category=category,
                        count=count
                    )
                    db.add(category_stat)
                else:
                    category_stat.count = count
        
        db.commit()
        print(f"\n✅ Статистика для {len(cities)} городов успешно обновлена!")
        
    finally:
        db.close()


if __name__ == "__main__":
    populate_city_stats_sync()