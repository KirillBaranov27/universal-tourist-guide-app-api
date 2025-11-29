from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.api.dependencies import get_current_user
from app.models.user import User
from app.models.landmark import Landmark
from app.schemas.favorite import (
    FavoriteCreate, 
    FavoriteResponse, 
    FavoriteListResponse,
    FavoriteWithLandmarkResponse
)
from app.crud.favorite_crud import (
    create_favorite,
    delete_favorite,
    get_user_favorites,
    is_landmark_favorite
)

router = APIRouter()


@router.get("/favorites", response_model=FavoriteListResponse)
def read_user_favorites(
    skip: int = Query(0, ge=0, description="Смещение для пагинации"),
    limit: int = Query(50, ge=1, le=100, description="Лимит записей"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Получить список избранных достопримечательностей пользователя.
    """
    favorites, total = get_user_favorites(
        db, user_id=current_user.id, skip=skip, limit=limit
    )
    
    # Преобразуем в ответ с информацией о достопримечательностях
    items = []
    for favorite in favorites:
        landmark = favorite.landmark
        items.append(FavoriteWithLandmarkResponse(
            id=favorite.id,
            user_id=favorite.user_id,
            landmark_id=favorite.landmark_id,
            created_at=favorite.created_at,
            landmark_name=landmark.name,
            landmark_city=landmark.city,
            landmark_image_url=landmark.image_url
        ))
    
    return FavoriteListResponse(items=items, total=total)


@router.post("/favorites", response_model=FavoriteResponse)
def add_to_favorites(
    favorite: FavoriteCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Добавить достопримечательность в избранное.
    """
    # Проверяем существование достопримечательности
    landmark = db.query(Landmark).filter(Landmark.id == favorite.landmark_id).first()
    if not landmark:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Достопримечательность не найдена"
        )
    
    db_favorite = create_favorite(db=db, favorite=favorite, user_id=current_user.id)
    return FavoriteResponse(
        id=db_favorite.id,
        user_id=db_favorite.user_id,
        landmark_id=db_favorite.landmark_id,
        created_at=db_favorite.created_at
    )


@router.delete("/favorites/{landmark_id}")
def remove_from_favorites(
    landmark_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Удалить достопримечательность из избранного.
    """
    success = delete_favorite(db, user_id=current_user.id, landmark_id=landmark_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Достопримечательность не найдена в избранном"
        )
    
    return {"message": "Достопримечательность удалена из избранного"}


@router.get("/favorites/check/{landmark_id}")
def check_favorite_status(
    landmark_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Проверить, находится ли достопримечательность в избранном.
    """
    is_favorite = is_landmark_favorite(db, user_id=current_user.id, landmark_id=landmark_id)
    return {"is_favorite": is_favorite}