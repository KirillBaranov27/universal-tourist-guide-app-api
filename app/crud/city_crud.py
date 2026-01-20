from sqlalchemy.orm import Session
from sqlalchemy import distinct, func, desc
from typing import Dict, List, Optional, Tuple
from app.models.landmark import Landmark
from app.models.review import Review
from app.models.discussion import Discussion

def get_city_profile(db: Session, city_name: str) -> Dict:
    """
    Получить профиль города с агрегированными данными
    """
    # Статистика по достопримечательностям
    landmarks_query = db.query(Landmark).filter(Landmark.city == city_name)
    total_landmarks = landmarks_query.count()
    
    # Получаем страну (берем первую попавшуюся, предполагая что город в одной стране)
    first_landmark = landmarks_query.first()
    country = first_landmark.country if first_landmark else "Неизвестно"
    
    # Распределение по категориям
    category_distribution = db.query(
        Landmark.category,
        func.count(Landmark.id).label('count')
    ).filter(
        Landmark.city == city_name
    ).group_by(
        Landmark.category
    ).order_by(
        desc('count')
    ).all()
    
    landmarks_by_category = {cat: count for cat, count in category_distribution}
    
    # Популярные категории (топ-5)
    popular_categories = [
        {"category": cat, "count": count}
        for cat, count in category_distribution[:5]
    ]
    
    # Статистика по отзывам
    total_reviews = db.query(Review).join(Landmark).filter(
        Landmark.city == city_name
    ).count()
    
    # Средний рейтинг города
    avg_rating_result = db.query(
        func.avg(Review.rating).label('avg_rating')
    ).join(Landmark).filter(
        Landmark.city == city_name
    ).first()
    
    average_rating = round(float(avg_rating_result.avg_rating or 0), 1) if avg_rating_result.avg_rating else None
    
    # Статистика по обсуждениям
    total_discussions = db.query(Discussion).filter(
        Discussion.city == city_name
    ).count()
    
    return {
        "city_name": city_name,
        "country": country,
        "total_landmarks": total_landmarks,
        "total_reviews": total_reviews,
        "total_discussions": total_discussions,
        "average_rating": average_rating,
        "popular_categories": popular_categories,
        "landmarks_by_category": landmarks_by_category
    }

def get_city_stats(db: Session, city_name: str) -> Dict:
    """
    Получить детальную статистику по городу
    """
    # Статистика по достопримечательностям
    landmarks_stats = {
        "total": db.query(Landmark).filter(Landmark.city == city_name).count(),
        "with_images": db.query(Landmark).filter(
            Landmark.city == city_name,
            Landmark.image_url.isnot(None)
        ).count(),
        "by_category": {}
    }
    
    # Статистика по отзывам
    reviews_stats = {
        "total": db.query(Review).join(Landmark).filter(Landmark.city == city_name).count(),
        "average_rating": db.query(
            func.avg(Review.rating)
        ).join(Landmark).filter(Landmark.city == city_name).scalar() or 0,
        "rating_distribution": {}
    }
    
    # Статистика по обсуждениям
    discussions_stats = {
        "total": db.query(Discussion).filter(Discussion.city == city_name).count(),
        "open": db.query(Discussion).filter(
            Discussion.city == city_name,
            Discussion.is_closed == False
        ).count(),
        "with_answers": db.query(func.count(distinct(Discussion.id))).filter(
            Discussion.city == city_name,
            Discussion.answers.any()
        ).scalar() or 0
    }
    
    return {
        "city_name": city_name,
        "landmarks_stats": landmarks_stats,
        "reviews_stats": reviews_stats,
        "discussions_stats": discussions_stats
    }

def get_cities_with_stats(db: Session, limit: int = 20) -> List[Dict]:
    """
    Получить список городов с базовой статистикой
    """
    cities_query = db.query(
        Landmark.city,
        Landmark.country,
        func.count(Landmark.id).label('landmark_count'),
        func.count(func.distinct(Review.id)).label('review_count')
    ).outerjoin(
        Review, Landmark.id == Review.landmark_id
    ).group_by(
        Landmark.city, Landmark.country
    ).order_by(
        desc('landmark_count')
    ).limit(limit)
    
    result = []
    for city, country, landmarks, reviews in cities_query.all():
        # Получаем одно изображение для города (первая достопримечательность с фото)
        sample_image = db.query(Landmark.image_url).filter(
            Landmark.city == city,
            Landmark.image_url.isnot(None)
        ).first()
        
        result.append({
            "city": city,
            "country": country,
            "landmark_count": landmarks,
            "review_count": reviews,
            "sample_image": sample_image[0] if sample_image else None
        })
    
    return result

def get_filtered_landmarks_by_city(
    db: Session,
    city: str,
    category: Optional[str] = None,
    min_rating: Optional[float] = None,
    price_filter: Optional[str] = None,
    has_images: Optional[bool] = None,
    skip: int = 0,
    limit: int = 50
) -> Tuple[List[Landmark], int]:
    """
    Получить отфильтрованные достопримечательности по городу
    """
    from sqlalchemy import and_, or_
    
    query = db.query(Landmark).filter(Landmark.city == city)
    
    # Дополнительные фильтры
    if category:
        query = query.filter(Landmark.category.ilike(f"%{category}%"))
    
    if min_rating:
        # Фильтр по минимальному рейтингу (через подзапрос)
        from sqlalchemy import select, func
        subquery = select(
            Review.landmark_id,
            func.avg(Review.rating).label('avg_rating')
        ).group_by(
            Review.landmark_id
        ).having(
            func.avg(Review.rating) >= min_rating
        ).subquery()
        
        query = query.join(subquery, Landmark.id == subquery.c.landmark_id)
    
    if has_images is not None:
        if has_images:
            query = query.filter(Landmark.image_url.isnot(None))
        else:
            query = query.filter(Landmark.image_url.is_(None))
    
    # Сортировка по рейтингу (если есть)
    if min_rating:
        query = query.order_by(desc(subquery.c.avg_rating))
    else:
        query = query.order_by(Landmark.name)
    
    # Пагинация
    total = query.count()
    landmarks = query.offset(skip).limit(limit).all()
    
    return landmarks, total

def get_city_categories(db: Session, city: str) -> List[str]:
    """
    Получить все уникальные категории для города
    """
    categories = db.query(Landmark.category).filter(
        Landmark.city == city
    ).distinct().all()
    
    return [category[0] for category in categories]