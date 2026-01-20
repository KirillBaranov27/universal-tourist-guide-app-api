from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime

class UserProfileBase(BaseModel):
    avatar_url: Optional[str] = Field(None, max_length=500, description="URL аватара")
    bio: Optional[str] = Field(None, max_length=2000, description="О себе")
    location: Optional[str] = Field(None, max_length=100, description="Местоположение")

class UserProfileUpdate(UserProfileBase):
    full_name: Optional[str] = Field(None, min_length=2, max_length=100, description="Полное имя")

class UserProfileResponse(UserProfileBase):
    id: int
    email: EmailStr
    full_name: str
    reputation_score: int = 0
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class UserStatsResponse(BaseModel):
    user_id: int
    total_reviews: int
    total_favorites: int
    helpful_answers: int = 0
    reputation_score: int
    reputation_level: str
    
    class Config:
        from_attributes = True