from typing import List, Optional, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, select

from app.core.database import get_db
from app.models.city import CityProfile, CityCategoryStats
from app.models.landmark import Landmark
from app.models.review import Review
from app.models.discussion import Discussion
from app.schemas.city import (
    CityProfileResponse, 
    CityStatsResponse, 
    PopularCityResponse
)

router = APIRouter()


@router.get("/profile/{city_name}", response_model=CityProfileResponse)
async def read_city_profile(
    city_name: str,
    db: Session = Depends(get_db)
):
    """Получить профиль города с агрегированной статистикой"""
    # Получаем профиль города
    city_profile = db.query(CityProfile).filter(
        CityProfile.city_name == city_name
    ).first()
    
    if not city_profile:
        # Если профиля нет, создаем базовую информацию
        landmark = db.query(Landmark).filter(
            Landmark.city == city_name
        ).first()
        
        if not landmark:
            raise HTTPException(status_code=404, detail="Город не найден")
        
        # Создаем базовый профиль
        city_profile = CityProfile(
            city_name=city_name,
            country=landmark.country
        )
        db.add(city_profile)
        db.commit()
        db.refresh(city_profile)
    
    # Получаем популярные категории (топ-5)
    category_stats = db.query(CityCategoryStats).filter(
        CityCategoryStats.city_name == city_name
    ).order_by(CityCategoryStats.count.desc()).limit(5).all()
    
    # Формируем список популярных категорий для response
    popular_categories = []
    for stat in category_stats:
        # Для каждой категории создаем словарь с именем и количеством
        popular_categories.append({
            "category": stat.category,
            "count": stat.count
        })
    
    # Формируем словарь категорий для landmarks_by_category
    landmarks_by_category = {}
    for stat in category_stats:
        landmarks_by_category[stat.category] = stat.count
    
    return {
        "city_name": city_profile.city_name,
        "country": city_profile.country,
        "description": city_profile.description,
        "image_url": city_profile.image_url,
        "total_landmarks": city_profile.total_landmarks,
        "total_reviews": city_profile.total_reviews,
        "total_discussions": city_profile.total_discussions,
        "average_rating": float(city_profile.average_rating) if city_profile.average_rating else 0.0,
        "popular_categories": popular_categories,
        "landmarks_by_category": landmarks_by_category,
        "created_at": city_profile.created_at,
        "updated_at": city_profile.updated_at
    }


@router.get("/stats/{city_name}", response_model=CityStatsResponse)
async def read_city_stats(
    city_name: str,
    db: Session = Depends(get_db)
):
    """Получить детальную статистику по городу"""
    # Получаем профиль города
    city_profile = db.query(CityProfile).filter(
        CityProfile.city_name == city_name
    ).first()
    
    if not city_profile:
        raise HTTPException(status_code=404, detail="Город не найден")
    
    # Получаем статистику по категориям
    category_stats = db.query(CityCategoryStats).filter(
        CityCategoryStats.city_name == city_name
    ).all()
    
    # Подсчитываем распределение рейтингов (от 1 до 5)
    rating_distribution = {}
    for i in range(1, 6):
        count = db.query(func.count()).filter(
            Review.landmark_id.in_(
                db.query(Landmark.id).filter(Landmark.city == city_name)
            ),
            Review.rating == i
        ).scalar()
        rating_distribution[str(i)] = count or 0
    
    # Получаем количество открытых/закрытых обсуждений
    open_discussions = db.query(func.count()).filter(
        Discussion.city == city_name,
        Discussion.is_closed == False
    ).scalar() or 0
    
    closed_discussions = db.query(func.count()).filter(
        Discussion.city == city_name,
        Discussion.is_closed == True
    ).scalar() or 0
    
    # Получаем количество обсуждений с ответами
    discussions_with_answers = db.query(func.count()).filter(
        Discussion.city == city_name,
        Discussion.answers.any()
    ).scalar() or 0
    
    # Получаем количество достопримечательностей с изображениями
    landmarks_with_images = db.query(func.count()).filter(
        Landmark.city == city_name,
        Landmark.image_url != None,
        Landmark.image_url != ""
    ).scalar() or 0
    
    # Формируем словари для категорий
    landmarks_by_category = {}
    for stat in category_stats:
        landmarks_by_category[stat.category] = stat.count
    
    # Формируем ответ
    return {
        "city_name": city_name,
        "landmarks_stats": {
            "total": city_profile.total_landmarks,
            "with_images": landmarks_with_images,
            "by_category": landmarks_by_category,
            "categories_count": len(category_stats)
        },
        "reviews_stats": {
            "total": city_profile.total_reviews,
            "average_rating": float(city_profile.average_rating) if city_profile.average_rating else 0.0,
            "rating_distribution": rating_distribution,
            "rating_levels": 5  # Максимальный рейтинг
        },
        "discussions_stats": {
            "total": city_profile.total_discussions,
            "open": open_discussions,
            "closed": closed_discussions,
            "with_answers": discussions_with_answers,
            "without_answers": city_profile.total_discussions - discussions_with_answers
        }
    }


@router.get("/popular", response_model=List[PopularCityResponse])
async def read_popular_cities(
    limit: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db)
):
    """Получить список популярных городов (по количеству достопримечательностей)"""
    # Получаем города с наибольшим количеством достопримечательностей
    cities = db.query(CityProfile).order_by(
        CityProfile.total_landmarks.desc()
    ).limit(limit).all()
    
    result = []
    for city in cities:
        result.append({
            "city_name": city.city_name,
            "country": city.country,
            "total_landmarks": city.total_landmarks,
            "average_rating": float(city.average_rating) if city.average_rating else 0.0,
            "image_url": city.image_url
        })
    
    return result


@router.get("/{city_name}/landmarks/filtered")
async def read_filtered_city_landmarks(
    city_name: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    category: Optional[str] = None,
    min_rating: Optional[float] = Query(None, ge=1, le=5),
    has_images: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    """Получить отфильтрованные достопримечательности города"""
    # Проверяем, существует ли город
    city_exists = db.query(Landmark).filter(Landmark.city == city_name).first()
    if not city_exists:
        raise HTTPException(status_code=404, detail="Город не найден")
    
    query = db.query(Landmark).filter(Landmark.city == city_name)
    
    # Применяем фильтры
    if category:
        query = query.filter(Landmark.category == category)
    
    if has_images is not None:
        if has_images:
            query = query.filter(
                Landmark.image_url != None, 
                Landmark.image_url != ""
            )
        else:
            query = query.filter(
                (Landmark.image_url == None) | (Landmark.image_url == "")
            )
    
    if min_rating is not None:
        # Находим достопримечательности с рейтингом выше указанного
        subquery = db.query(Review.landmark_id).filter(
            Review.landmark_id == Landmark.id
        ).group_by(Review.landmark_id).having(
            func.avg(Review.rating) >= min_rating
        ).subquery()
        
        query = query.filter(Landmark.id.in_(select(subquery.c.landmark_id)))
    
    # Считаем общее количество
    total = query.count()
    
    # Применяем пагинацию
    landmarks = query.offset(skip).limit(limit).all()
    
    # Рассчитываем количество страниц
    pages = (total + limit - 1) // limit if limit > 0 else 0
    page = skip // limit if limit > 0 else 0
    
    return {
        "items": landmarks,
        "total": total,
        "page": page,
        "size": len(landmarks),
        "pages": pages
    }


@router.get("/{city_name}/categories", response_model=List[str])
async def read_city_categories(
    city_name: str,
    db: Session = Depends(get_db)
):
    """Получить все категории достопримечательностей для города"""
    # Проверяем, существует ли город
    city_exists = db.query(Landmark).filter(Landmark.city == city_name).first()
    if not city_exists:
        raise HTTPException(status_code=404, detail="Город не найден")
    
    categories = db.query(Landmark.category).filter(
        Landmark.city == city_name
    ).distinct().all()
    
    return [category[0] for category in categories if category[0]]


@router.get("/{city_name}/discussions")
async def read_city_discussions(
    city_name: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    only_open: bool = Query(False),
    db: Session = Depends(get_db)
):
    """Получить обсуждения, связанные с городом"""
    # Проверяем, существует ли город
    city_exists = db.query(Landmark).filter(Landmark.city == city_name).first()
    if not city_exists:
        raise HTTPException(status_code=404, detail="Город не найден")
    
    query = db.query(Discussion).filter(Discussion.city == city_name)
    
    if only_open:
        query = query.filter(Discussion.is_closed == False)
    
    # Считаем общее количество
    total = query.count()
    
    # Применяем пагинацию и сортировку
    discussions = query.order_by(
        Discussion.created_at.desc()
    ).offset(skip).limit(limit).all()
    
    return {
        "items": discussions,
        "total": total,
        "page": skip // limit if limit > 0 else 0,
        "size": len(discussions),
        "pages": (total + limit - 1) // limit if limit > 0 else 0
    }


@router.post("/{city_name}/landmarks/search")
async def search_city_landmarks(
    city_name: str,
    search: str = Query(..., min_length=1),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Поиск достопримечательностей в городе"""
    # Проверяем, существует ли город
    city_exists = db.query(Landmark).filter(Landmark.city == city_name).first()
    if not city_exists:
        raise HTTPException(status_code=404, detail="Город не найден")
    
    query = db.query(Landmark).filter(
        Landmark.city == city_name,
        (
            Landmark.name.ilike(f"%{search}%") |
            Landmark.description.ilike(f"%{search}%")
        )
    )
    
    # Считаем общее количество
    total = query.count()
    
    # Применяем пагинацию
    landmarks = query.offset(skip).limit(limit).all()
    
    return {
        "items": landmarks,
        "total": total,
        "page": skip // limit if limit > 0 else 0,
        "size": len(landmarks),
        "pages": (total + limit - 1) // limit if limit > 0 else 0
    }