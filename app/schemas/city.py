from pydantic import BaseModel
from typing import List, Dict, Optional, Any
from datetime import datetime


class CategoryStat(BaseModel):
    category: str
    count: int

    class Config:
        from_attributes = True


class CityBase(BaseModel):
    city_name: str
    country: str
    description: Optional[str] = None
    image_url: Optional[str] = None

    class Config:
        from_attributes = True


class CityProfileResponse(BaseModel):
    city_name: str
    country: str
    total_landmarks: int
    total_reviews: int
    total_discussions: int
    average_rating: float
    popular_categories: List[CategoryStat]
    landmarks_by_category: Dict[str, int]
    description: Optional[str] = None
    image_url: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class CityStatsResponse(BaseModel):
    city_name: str
    landmarks_stats: Dict[str, Any]
    reviews_stats: Dict[str, Any]
    discussions_stats: Dict[str, Any]

    class Config:
        from_attributes = True


class PopularCityResponse(BaseModel):
    city_name: str
    country: str
    total_landmarks: int
    average_rating: float
    image_url: Optional[str] = None

    class Config:
        from_attributes = True


class CityFilters(BaseModel):
    cities: List[str]
    categories: List[str]

    class Config:
        from_attributes = True