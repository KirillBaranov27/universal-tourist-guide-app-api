from typing import Optional
from pydantic import BaseModel
from datetime import datetime


class FavoriteBase(BaseModel):
    landmark_id: int


class FavoriteCreate(FavoriteBase):
    pass


class FavoriteResponse(FavoriteBase):
    id: int
    user_id: int
    created_at: datetime
    landmark_name: str
    landmark_city: str
    landmark_image_url: Optional[str] = None

    class Config:
        from_attributes = True


# Для совместимости
class Favorite(FavoriteResponse):
    pass