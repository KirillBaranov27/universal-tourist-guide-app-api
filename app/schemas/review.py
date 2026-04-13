from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class ReviewBase(BaseModel):
    landmark_id: int
    rating: float = Field(..., ge=1, le=5)
    comment: Optional[str] = None


class ReviewCreate(ReviewBase):
    pass


class ReviewUpdate(BaseModel):
    rating: Optional[float] = Field(None, ge=1, le=5)
    comment: Optional[str] = None


class ReviewResponse(ReviewBase):
    id: int
    user_id: int
    user_name: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Для совместимости
class Review(ReviewResponse):
    pass