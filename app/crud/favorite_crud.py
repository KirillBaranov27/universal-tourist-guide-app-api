from sqlalchemy.orm import Session, joinedload
from typing import List, Tuple
from app.models.favorite import Favorite
from app.models.landmark import Landmark
from app.schemas.favorite import FavoriteCreate


def get_favorite(db: Session, user_id: int, landmark_id: int) -> Favorite | None:
    """
    Получить запись избранного по пользователю и достопримечательности
    """
    return db.query(Favorite).filter(
        Favorite.user_id == user_id,
        Favorite.landmark_id == landmark_id
    ).first()


def get_user_favorites(
    db: Session, 
    user_id: int, 
    skip: int = 0, 
    limit: int = 100
) -> Tuple[List[Favorite], int]:
    """
    Получить список избранных достопримечательностей пользователя
    """
    query = db.query(Favorite).filter(Favorite.user_id == user_id)
    total = query.count()
    
    # Исправлено: добавляем joinedload для загрузки связанных данных
    favorites = query.options(joinedload(Favorite.landmark))\
                    .offset(skip)\
                    .limit(limit)\
                    .all()
    
    return favorites, total


def create_favorite(db: Session, favorite: FavoriteCreate, user_id: int) -> Favorite:
    """
    Добавить достопримечательность в избранное
    """
    # Проверяем, не добавлена ли уже эта достопримечательность
    existing_favorite = get_favorite(db, user_id, favorite.landmark_id)
    if existing_favorite:
        return existing_favorite

    db_favorite = Favorite(**favorite.dict(), user_id=user_id)
    db.add(db_favorite)
    db.commit()
    db.refresh(db_favorite)
    return db_favorite


def delete_favorite(db: Session, user_id: int, landmark_id: int) -> bool:
    """
    Удалить достопримечательность из избранного
    """
    db_favorite = get_favorite(db, user_id, landmark_id)
    if not db_favorite:
        return False

    db.delete(db_favorite)
    db.commit()
    return True


def is_landmark_favorite(db: Session, user_id: int, landmark_id: int) -> bool:
    """
    Проверить, находится ли достопримечательность в избранном у пользователя
    """
    favorite = get_favorite(db, user_id, landmark_id)
    return favorite is not None