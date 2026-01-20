from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from typing import Optional, List, Tuple
from app.models.landmark import Landmark
from app.schemas.landmark import LandmarkCreate, LandmarkUpdate


def get_landmark(db: Session, landmark_id: int) -> Optional[Landmark]:
    """
    Получить достопримечательность по ID
    """
    return db.query(Landmark).filter(Landmark.id == landmark_id).first()


def get_landmarks(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    city: Optional[str] = None,
    country: Optional[str] = None,
    category: Optional[str] = None,
    search: Optional[str] = None
) -> Tuple[List[Landmark], int]:
    """
    Получить список достопримечательностей с фильтрацией и пагинацией
    """
    query = db.query(Landmark)

    # Применяем фильтры
    if city:
        query = query.filter(Landmark.city.ilike(f"%{city}%"))
    if country:
        query = query.filter(Landmark.country.ilike(f"%{country}%"))
    if category:
        query = query.filter(Landmark.category.ilike(f"%{category}%"))
    if search:
        search_filter = or_(
            Landmark.name.ilike(f"%{search}%"),
            Landmark.description.ilike(f"%{search}%"),
            Landmark.city.ilike(f"%{search}%")
        )
        query = query.filter(search_filter)

    # Получаем общее количество для пагинации
    total = query.count()

    # Применяем пагинацию
    landmarks = query.offset(skip).limit(limit).all()

    return landmarks, total


def create_landmark(db: Session, landmark: LandmarkCreate) -> Landmark:
    """
    Создать новую достопримечательность
    """
    db_landmark = Landmark(**landmark.dict())
    db.add(db_landmark)
    db.commit()
    db.refresh(db_landmark)
    return db_landmark


def update_landmark(
    db: Session,
    landmark_id: int,
    landmark: LandmarkUpdate
) -> Optional[Landmark]:
    """
    Обновить информацию о достопримечательности
    """
    db_landmark = db.query(Landmark).filter(Landmark.id == landmark_id).first()
    if not db_landmark:
        return None

    # Обновляем только переданные поля
    update_data = landmark.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_landmark, field, value)

    db.commit()
    db.refresh(db_landmark)
    return db_landmark

def delete_landmark(db: Session, landmark_id: int) -> bool:
    """
    Удалить достопримечательность
    """
    db_landmark = db.query(Landmark).filter(Landmark.id == landmark_id).first()
    if not db_landmark:
        return False

    db.delete(db_landmark)
    db.commit()
    return True


def get_cities(db: Session) -> List[str]:
    """
    Получить список уникальных городов
    """
    cities = db.query(Landmark.city).distinct().all()
    return [city[0] for city in cities]


def get_categories(db: Session) -> List[str]:
    """
    Получить список уникальных категорий
    """
    categories = db.query(Landmark.category).distinct().all()
    return [category[0] for category in categories]


def get_landmarks_near_location(
    db: Session,
    latitude: float,
    longitude: float,
    radius_km: float = 10,
    limit: int = 50
) -> List[Landmark]:
    """
    Получить достопримечательности в радиусе от указанных координат
    (Упрощенная версия - в продакшене лучше использовать PostGIS)
    """
    # Простая формула гаверсинуса для расчета расстояния
    landmarks = db.query(Landmark).all()

    def calculate_distance(lat1, lon1, lat2, lon2):
        # Упрощенный расчет расстояния
        return ((lat1 - lat2) ** 2 + (lon1 - lon2) ** 2) ** 0.5 * 111  # примерно км

    nearby_landmarks = []
    for landmark in landmarks:
        distance = calculate_distance(
            latitude, longitude,
            landmark.latitude, landmark.longitude
        )
        if distance <= radius_km:
            landmark.distance = distance  # type: ignore
            nearby_landmarks.append(landmark)

    # Сортируем по расстоянию и ограничиваем количество
    nearby_landmarks.sort(key=lambda x: x.distance)  # type: ignore
    return nearby_landmarks[:limit]