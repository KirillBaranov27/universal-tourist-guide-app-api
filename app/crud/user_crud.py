from sqlalchemy.orm import Session
from typing import Optional, List, Tuple
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.schemas.profile import UserProfileUpdate
from app.core.security import get_password_hash


def get_user(db: Session, user_id: int) -> Optional[User]:
    """
    Получить пользователя по ID
    """
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """
    Получить пользователя по email
    """
    return db.query(User).filter(User.email == email).first()


def create_user(db: Session, user: UserCreate) -> User:
    """
    Создать нового пользователя
    """
    db_user = User(
        email=user.email,
        hashed_password=get_password_hash(user.password),
        full_name=user.full_name
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, user_id: int, user_update: UserUpdate) -> Optional[User]:
    """
    Обновить информацию о пользователе
    """
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        return None
    
    update_data = user_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_user, field, value)
    
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int) -> bool:
    """
    Удалить пользователя
    """
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        return False
    
    db.delete(db_user)
    db.commit()
    return True


def get_users(db: Session, skip: int = 0, limit: int = 100) -> Tuple[List[User], int]:
    """
    Получить список пользователей
    """
    query = db.query(User)
    total = query.count()
    users = query.offset(skip).limit(limit).all()
    return users, total


def get_user_profile(db: Session, user_id: int) -> Optional[User]:
    """
    Получить профиль пользователя (алиас для get_user для совместимости)
    """
    return get_user(db, user_id)


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
    from app.models.discussion import Discussion, DiscussionAnswer
    
    total_reviews = db.query(Review).filter(Review.user_id == user_id).count()
    total_favorites = db.query(Favorite).filter(Favorite.user_id == user_id).count()
    total_discussions = db.query(Discussion).filter(Discussion.user_id == user_id).count()
    
    # Получаем полезные ответы (где is_helpful=True)
    helpful_answers = db.query(DiscussionAnswer).filter(
        DiscussionAnswer.user_id == user_id,
        DiscussionAnswer.is_helpful == True
    ).count()
    
    # Получаем общее количество ответов пользователя
    total_answers = db.query(DiscussionAnswer).filter(
        DiscussionAnswer.user_id == user_id
    ).count()
    
    # Получаем пользователя для репутации
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return {}
    
    # Вычисляем репутацию
    reputation_score = user.reputation_score
    
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
        "total_discussions": total_discussions,
        "total_answers": total_answers,
        "helpful_answers": helpful_answers,
        "reputation_score": reputation_score,
        "reputation_level": reputation_level
    }