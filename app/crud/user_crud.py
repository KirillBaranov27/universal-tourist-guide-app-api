from sqlalchemy.orm import Session
from typing import Optional
from app.models.user import User
from app.schemas.profile import UserProfileUpdate

def get_user_profile(db: Session, user_id: int) -> Optional[User]:
    """
    Получить профиль пользователя
    """
    return db.query(User).filter(User.id == user_id).first()

def update_user_profile(
    db: Session, 
    user_id: int, 
    profile_update: UserProfileUpdate
) -> Optional[User]:
    """
    Обновить профиль пользователя
    """
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        return None
    
    update_data = profile_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        if value is not None:
            setattr(db_user, field, value)
    
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_stats(db: Session, user_id: int) -> dict:
    """
    Получить статистику пользователя
    """
    from app.models.review import Review
    from app.models.favorite import Favorite
    from app.crud.discussion_crud import get_discussion_stats
    
    total_reviews = db.query(Review).filter(Review.user_id == user_id).count()
    total_favorites = db.query(Favorite).filter(Favorite.user_id == user_id).count()
    
    # Получаем статистику по обсуждениям
    discussion_stats = get_discussion_stats(db, user_id)
    helpful_answers = discussion_stats.get("helpful_answers", 0)
    
    # Вычисляем репутацию с учётом обсуждений
    reputation_score = (
        total_reviews * 5 + 
        total_favorites * 2 + 
        helpful_answers * 10 +
        discussion_stats.get("total_discussions", 0) * 5 +
        discussion_stats.get("total_answers", 0) * 2
    )
    
    # Уровень репутации
    if reputation_score >= 200:
        reputation_level = "Эксперт-гид"
    elif reputation_score >= 100:
        reputation_level = "Эксперт"
    elif reputation_score >= 50:
        reputation_level = "Активный путешественник"
    elif reputation_score >= 20:
        reputation_level = "Путешественник"
    else:
        reputation_level = "Новичок"
    
    return {
        "user_id": user_id,
        "total_reviews": total_reviews,
        "total_favorites": total_favorites,
        "total_discussions": discussion_stats.get("total_discussions", 0),
        "total_answers": discussion_stats.get("total_answers", 0),
        "helpful_answers": helpful_answers,
        "reputation_score": reputation_score,
        "reputation_level": reputation_level
    }