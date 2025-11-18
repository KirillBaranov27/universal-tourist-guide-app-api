from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class LandmarkBase(BaseModel):
    """Базовая схема достопримечательности"""
    name: str
    description: Optional[str] = None
    short_description: Optional[str] = None
    latitude: float
    longitude: float
    city: str
    category: Optional[str] = None
    rating: Optional[float] = None
    image_url: Optional[str] = None
    audio_url: Optional[str] = None

class LandmarkCreate(LandmarkBase):
    """Схема для создания достопримечательности"""
    pass

class LandmarkResponse(LandmarkBase):
    """Схема ответа с данными достопримечательности"""
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True