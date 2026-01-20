from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.api.dependencies import get_current_user
from app.models.user import User
from app.schemas.profile import UserProfileResponse, UserProfileUpdate, UserStatsResponse
from app.crud.user_crud import get_user_profile, update_user_profile, get_user_stats

router = APIRouter()

@router.get("/profile", response_model=UserProfileResponse)
def read_user_profile(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Получить профиль текущего пользователя
    """
    user_profile = get_user_profile(db, user_id=current_user.id)
    if not user_profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь не найден"
        )
    return user_profile

@router.put("/profile", response_model=UserProfileResponse)
def update_profile(
    profile_update: UserProfileUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Обновить профиль пользователя
    """
    updated_user = update_user_profile(
        db, 
        user_id=current_user.id, 
        profile_update=profile_update
    )
    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь не найден"
        )
    return updated_user

@router.get("/profile/stats", response_model=UserStatsResponse)
def get_profile_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Получить статистику пользователя
    """
    stats = get_user_stats(db, user_id=current_user.id)
    return stats

@router.get("/users/{user_id}/profile", response_model=UserProfileResponse)
def read_public_profile(
    user_id: int,
    db: Session = Depends(get_db)
):
    """
    Получить публичный профиль пользователя (доступно всем)
    """
    user_profile = get_user_profile(db, user_id=user_id)
    if not user_profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь не найден"
        )
    return user_profile

@router.get("/users/{user_id}/stats", response_model=UserStatsResponse)
def get_public_stats(
    user_id: int,
    db: Session = Depends(get_db)
):
    """
    Получить публичную статистику пользователя
    """
    stats = get_user_stats(db, user_id=user_id)
    return stats