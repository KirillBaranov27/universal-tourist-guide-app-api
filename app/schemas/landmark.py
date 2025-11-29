from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class LandmarkBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255, description="Название достопримечательности")
    description: Optional[str] = Field(None, description="Описание")
    city: str = Field(..., min_length=1, max_length=100, description="Город")
    country: str = Field(..., min_length=1, max_length=100, description="Страна")
    category: str = Field(..., min_length=1, max_length=100, description="Категория")
    latitude: float = Field(..., ge=-90, le=90, description="Широта")
    longitude: float = Field(..., ge=-180, le=180, description="Долгота")
    address: Optional[str] = Field(None, max_length=500, description="Адрес")
    image_url: Optional[str] = Field(None, max_length=500, description="URL изображения")


class LandmarkCreate(LandmarkBase):
    pass


class LandmarkUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    city: Optional[str] = Field(None, min_length=1, max_length=100)
    country: Optional[str] = Field(None, min_length=1, max_length=100)
    category: Optional[str] = Field(None, min_length=1, max_length=100)
    latitude: Optional[float] = Field(None, ge=-90, le=90)
    longitude: Optional[float] = Field(None, ge=-180, le=180)
    address: Optional[str] = Field(None, max_length=500)
    image_url: Optional[str] = Field(None, max_length=500)


class LandmarkResponse(LandmarkBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class LandmarkWithDistance(LandmarkResponse):
    distance: Optional[float] = None


class LandmarkListResponse(BaseModel):
    items: List[LandmarkResponse]
    total: int
    page: int
    size: int
    pages: int


class FiltersResponse(BaseModel):
    cities: List[str]
    categories: List[str]