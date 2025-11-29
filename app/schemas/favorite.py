from pydantic import BaseModel
from datetime import datetime
from typing import List

class FavoriteBase(BaseModel):
    landmark_id: int

class FavoriteCreate(FavoriteBase):
    pass

class FavoriteResponse(FavoriteBase):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True

class FavoriteWithLandmarkResponse(FavoriteResponse):
    landmark_name: str
    landmark_city: str
    landmark_image_url: str | None

class FavoriteListResponse(BaseModel):
    items: List[FavoriteWithLandmarkResponse]
    total: int