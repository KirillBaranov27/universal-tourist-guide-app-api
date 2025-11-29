from sqlalchemy.orm import Session, joinedload
from typing import List, Tuple, Optional, Dict
from app.models.review import Review
from app.models.user import User
from app.models.landmark import Landmark
from app.schemas.review import ReviewCreate, ReviewUpdate


def get_review(db: Session, user_id: int, landmark_id: int) -> Review | None:
    """
    Получить отзыв пользователя для достопримечательности
    """
    return db.query(Review).filter(
        Review.user_id == user_id,
        Review.landmark_id == landmark_id
    ).first()


def get_reviews_by_landmark(
    db: Session, 
    landmark_id: int, 
    skip: int = 0, 
    limit: int = 100
) -> Tuple[List[Review], int]:
    """
    Получить все отзывы для достопримечательности
    """
    query = db.query(Review).filter(Review.landmark_id == landmark_id)
    total = query.count()
    
    # Исправлено: добавляем joinedload для загрузки связанных данных
    reviews = query.options(joinedload(Review.user))\
                  .order_by(Review.created_at.desc())\
                  .offset(skip)\
                  .limit(limit)\
                  .all()
    
    return reviews, total


def get_reviews_by_user(
    db: Session, 
    user_id: int, 
    skip: int = 0, 
    limit: int = 100
) -> Tuple[List[Review], int]:
    """
    Получить все отзывы пользователя
    """
    query = db.query(Review).filter(Review.user_id == user_id)
    total = query.count()
    
    # Исправлено: добавляем joinedload для загрузки связанных данных
    reviews = query.options(joinedload(Review.landmark))\
                  .order_by(Review.created_at.desc())\
                  .offset(skip)\
                  .limit(limit)\
                  .all()
    
    return reviews, total


def create_review(db: Session, review: ReviewCreate, user_id: int) -> Review:
    """
    Создать новый отзыв
    """
    # Проверяем, не оставил ли пользователь уже отзыв
    existing_review = get_review(db, user_id, review.landmark_id)
    if existing_review:
        # Если отзыв существует, обновляем его
        return update_review(db, user_id, review.landmark_id, ReviewUpdate(**review.dict()))

    db_review = Review(**review.dict(), user_id=user_id)
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review


def update_review(
    db: Session, 
    user_id: int, 
    landmark_id: int, 
    review: ReviewUpdate
) -> Review | None:
    """
    Обновить отзыв
    """
    db_review = get_review(db, user_id, landmark_id)
    if not db_review:
        return None

    update_data = review.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_review, field, value)

    db.commit()
    db.refresh(db_review)
    return db_review


def delete_review(db: Session, user_id: int, landmark_id: int) -> bool:
    """
    Удалить отзыв
    """
    db_review = get_review(db, user_id, landmark_id)
    if not db_review:
        return False

    db.delete(db_review)
    db.commit()
    return True


def get_landmark_rating_summary(db: Session, landmark_id: int) -> Tuple[Optional[float], int, Dict[int, int]]:
    """
    Получить сводку по рейтингам достопримечательности
    """
    reviews = db.query(Review).filter(Review.landmark_id == landmark_id).all()
    
    if not reviews:
        return None, 0, {}

    total_rating = sum(review.rating for review in reviews)
    average_rating = round(total_rating / len(reviews), 1)
    
    # Распределение оценок
    rating_distribution = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
    for review in reviews:
        rating = int(review.rating)
        rating_distribution[rating] = rating_distribution.get(rating, 0) + 1

    return average_rating, len(reviews), rating_distribution