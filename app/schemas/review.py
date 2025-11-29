from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List

class ReviewBase(BaseModel):
    landmark_id: int
    rating: float = Field(..., ge=1, le=5, description="Оценка от 1 до 5")
    comment: Optional[str] = Field(None, max_length=1000, description="Текст отзыва")

class ReviewCreate(ReviewBase):
    pass

class ReviewUpdate(BaseModel):
    rating: Optional[float] = Field(None, ge=1, le=5)
    comment: Optional[str] = Field(None, max_length=1000)

class ReviewResponse(ReviewBase):
    id: int
    user_id: int
    user_name: str
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True

class ReviewWithLandmarkResponse(ReviewResponse):
    landmark_name: str
    landmark_city: str

class ReviewListResponse(BaseModel):
    items: List[ReviewResponse]
    total: int

class LandmarkReviewSummary(BaseModel):
    average_rating: Optional[float] = None
    total_reviews: int
    rating_distribution: dict[int, int]  # Распределение оценок