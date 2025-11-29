from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional, List

from app.core.database import get_db
from app.api.dependencies import get_current_user
from app.models.user import User
from app.schemas.landmark import (
    LandmarkResponse,
    LandmarkCreate,
    LandmarkUpdate,
    LandmarkListResponse,
    FiltersResponse,
    LandmarkWithDistance
)
from app.crud.landmark_crud import (
    get_landmark,
    get_landmarks,
    create_landmark,
    update_landmark,
    delete_landmark,
    get_cities,
    get_categories,
    get_landmarks_near_location
)

router = APIRouter()


@router.get("/landmarks", response_model=LandmarkListResponse)
def read_landmarks(
    skip: int = Query(0, ge=0, description="Смещение для пагинации"),
    limit: int = Query(50, ge=1, le=100, description="Лимит записей на странице"),
    city: Optional[str] = Query(None, description="Фильтр по городу"),
    country: Optional[str] = Query(None, description="Фильтр по стране"),
    category: Optional[str] = Query(None, description="Фильтр по категории"),
    search: Optional[str] = Query(None, description="Поиск по названию и описанию"),
    db: Session = Depends(get_db)
):
    """
    Получить список достопримечательностей с пагинацией и фильтрацией.
    """
    landmarks, total = get_landmarks(
        db,
        skip=skip,
        limit=limit,
        city=city,
        country=country,
        category=category,
        search=search
    )

    # Рассчитываем пагинацию
    pages = (total + limit - 1) // limit if limit > 0 else 1
    current_page = (skip // limit) + 1 if limit > 0 else 1

    return LandmarkListResponse(
        items=landmarks,
        total=total,
        page=current_page,
        size=limit,
        pages=pages
    )


@router.get("/landmarks/nearby", response_model=List[LandmarkWithDistance])
def get_nearby_landmarks(
    latitude: float = Query(..., description="Широта текущего местоположения"),
    longitude: float = Query(..., description="Долгота текущего местоположения"),
    radius: float = Query(10, ge=1, le=100, description="Радиус поиска в км"),
    limit: int = Query(20, ge=1, le=100, description="Максимальное количество результатов"),
    db: Session = Depends(get_db)
):
    """
    Найти достопримечательности поблизости от указанных координат.
    """
    landmarks = get_landmarks_near_location(
        db=db,
        latitude=latitude,
        longitude=longitude,
        radius_km=radius,
        limit=limit
    )
    return landmarks


@router.get("/landmarks/{landmark_id}", response_model=LandmarkResponse)
def read_landmark(
    landmark_id: int,
    db: Session = Depends(get_db)
):
    """
    Получить детальную информацию о достопримечательности по ID.
    """
    db_landmark = get_landmark(db, landmark_id=landmark_id)
    if db_landmark is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Достопримечательность не найдена"
        )
    return db_landmark


@router.post("/landmarks", response_model=LandmarkResponse)
def create_new_landmark(
    landmark: LandmarkCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Создать новую достопримечательность (требуется аутентификация).
    """
    return create_landmark(db=db, landmark=landmark)


@router.put("/landmarks/{landmark_id}", response_model=LandmarkResponse)
def update_existing_landmark(
    landmark_id: int,
    landmark: LandmarkUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Обновить информацию о достопримечательности (требуется аутентификация).
    """
    db_landmark = update_landmark(
        db=db,
        landmark_id=landmark_id,
        landmark=landmark
    )
    if db_landmark is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Достопримечательность не найдена"
        )
    return db_landmark


@router.delete("/landmarks/{landmark_id}")
def delete_existing_landmark(
    landmark_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Удалить достопримечательность (требуется аутентификация).
    """
    success = delete_landmark(db=db, landmark_id=landmark_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Достопримечательность не найдена"
        )
    return {"message": "Достопримечательность успешно удалена"}


@router.get("/landmarks/filters/cities", response_model=List[str])
def get_available_cities(db: Session = Depends(get_db)):
    """
    Получить список всех доступных городов.
    """
    return get_cities(db)


@router.get("/landmarks/filters/categories", response_model=List[str])
def get_available_categories(db: Session = Depends(get_db)):
    """
    Получить список всех доступных категорий.
    """
    return get_categories(db)


@router.get("/filters/all", response_model=FiltersResponse)
def get_all_filters(db: Session = Depends(get_db)):
    """
    Получить все доступные фильтры (города и категории).
    """
    cities = get_cities(db)
    categories = get_categories(db)
    return FiltersResponse(cities=cities, categories=categories)