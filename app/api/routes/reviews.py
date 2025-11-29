from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.api.dependencies import get_current_user
from app.models.user import User
from app.models.landmark import Landmark
from app.schemas.review import (
    ReviewCreate,
    ReviewUpdate,
    ReviewResponse,
    ReviewListResponse,
    ReviewWithLandmarkResponse,
    LandmarkReviewSummary
)
from app.crud.review_crud import (
    create_review,
    update_review,
    delete_review,
    get_reviews_by_landmark,
    get_reviews_by_user,
    get_landmark_rating_summary
)

router = APIRouter()


@router.get("/reviews/landmark/{landmark_id}", response_model=ReviewListResponse)
def read_landmark_reviews(
    landmark_id: int,
    skip: int = Query(0, ge=0, description="Смещение для пагинации"),
    limit: int = Query(50, ge=1, le=100, description="Лимит записей"),
    db: Session = Depends(get_db)
):
    """
    Получить все отзывы для достопримечательности.
    """
    reviews, total = get_reviews_by_landmark(
        db, landmark_id=landmark_id, skip=skip, limit=limit
    )
    
    # Преобразуем в ответ с информацией о пользователях
    items = []
    for review in reviews:
        items.append(ReviewResponse(
            id=review.id,
            user_id=review.user_id,
            user_name=review.user.full_name,
            landmark_id=review.landmark_id,
            rating=review.rating,
            comment=review.comment,
            created_at=review.created_at,
            updated_at=review.updated_at
        ))
    
    return ReviewListResponse(items=items, total=total)


@router.get("/reviews/user", response_model=ReviewListResponse)
def read_user_reviews(
    skip: int = Query(0, ge=0, description="Смещение для пагинации"),
    limit: int = Query(50, ge=1, le=100, description="Лимит записей"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Получить все отзывы текущего пользователя.
    """
    reviews, total = get_reviews_by_user(
        db, user_id=current_user.id, skip=skip, limit=limit
    )
    
    # Преобразуем в ответ с информацией о достопримечательностях
    items = []
    for review in reviews:
        items.append(ReviewWithLandmarkResponse(
            id=review.id,
            user_id=review.user_id,
            user_name=current_user.full_name,
            landmark_id=review.landmark_id,
            landmark_name=review.landmark.name,
            landmark_city=review.landmark.city,
            rating=review.rating,
            comment=review.comment,
            created_at=review.created_at,
            updated_at=review.updated_at
        ))
    
    return ReviewListResponse(items=items, total=total)


@router.post("/reviews", response_model=ReviewResponse)
def create_new_review(
    review: ReviewCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Создать новый отзыв.
    """
    # Проверяем существование достопримечательности
    landmark = db.query(Landmark).filter(Landmark.id == review.landmark_id).first()
    if not landmark:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Достопримечательность не найдена"
        )
    
    db_review = create_review(db=db, review=review, user_id=current_user.id)
    
    return ReviewResponse(
        id=db_review.id,
        user_id=db_review.user_id,
        user_name=current_user.full_name,
        landmark_id=db_review.landmark_id,
        rating=db_review.rating,
        comment=db_review.comment,
        created_at=db_review.created_at,
        updated_at=db_review.updated_at
    )


@router.put("/reviews/{landmark_id}", response_model=ReviewResponse)
def update_existing_review(
    landmark_id: int,
    review: ReviewUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Обновить отзыв для достопримечательности.
    """
    db_review = update_review(
        db, user_id=current_user.id, landmark_id=landmark_id, review=review
    )
    
    if db_review is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Отзыв не найден"
        )
    
    return ReviewResponse(
        id=db_review.id,
        user_id=db_review.user_id,
        user_name=current_user.full_name,
        landmark_id=db_review.landmark_id,
        rating=db_review.rating,
        comment=db_review.comment,
        created_at=db_review.created_at,
        updated_at=db_review.updated_at
    )


@router.delete("/reviews/{landmark_id}")
def delete_existing_review(
    landmark_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Удалить отзыв для достопримечательности.
    """
    success = delete_review(db, user_id=current_user.id, landmark_id=landmark_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Отзыв не найден"
        )
    
    return {"message": "Отзыв успешно удален"}


@router.get("/reviews/landmark/{landmark_id}/summary", response_model=LandmarkReviewSummary)
def get_review_summary(
    landmark_id: int,
    db: Session = Depends(get_db)
):
    """
    Получить сводку по отзывам для достопримечательности.
    """
    average_rating, total_reviews, rating_distribution = get_landmark_rating_summary(
        db, landmark_id
    )
    
    return LandmarkReviewSummary(
        average_rating=average_rating,
        total_reviews=total_reviews,
        rating_distribution=rating_distribution
    )