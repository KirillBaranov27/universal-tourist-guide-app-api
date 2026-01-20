from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

# Базовые схемы
class DiscussionBase(BaseModel):
    title: str = Field(..., min_length=5, max_length=200, description="Заголовок обсуждения")
    content: str = Field(..., min_length=10, max_length=5000, description="Содержание обсуждения")
    landmark_id: Optional[int] = Field(None, description="ID достопримечательности (если привязано)")
    city: Optional[str] = Field(None, max_length=100, description="Город (если обсуждение о городе)")

class DiscussionCreate(DiscussionBase):
    pass

class DiscussionUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=5, max_length=200)
    content: Optional[str] = Field(None, min_length=10, max_length=5000)
    is_closed: Optional[bool] = None

class DiscussionResponse(DiscussionBase):
    id: int
    user_id: int
    user_name: str
    user_avatar: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    is_closed: bool
    answer_count: int = 0
    
    class Config:
        from_attributes = True

class DiscussionWithAnswersResponse(DiscussionResponse):
    answers: List["DiscussionAnswerResponse"] = []

# Схемы для ответов
class DiscussionAnswerBase(BaseModel):
    content: str = Field(..., min_length=5, max_length=2000, description="Текст ответа")

class DiscussionAnswerCreate(DiscussionAnswerBase):
    pass

class DiscussionAnswerUpdate(BaseModel):
    content: Optional[str] = Field(None, min_length=5, max_length=2000)

class DiscussionAnswerResponse(DiscussionAnswerBase):
    id: int
    user_id: int
    user_name: str
    user_avatar: Optional[str] = None
    discussion_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    is_helpful: bool
    helpful_votes: int
    
    class Config:
        from_attributes = True

# Схемы для списков
class DiscussionListResponse(BaseModel):
    items: List[DiscussionResponse]
    total: int
    page: int
    size: int
    pages: int

class AnswerListResponse(BaseModel):
    items: List[DiscussionAnswerResponse]
    total: int

# Схема для голосования
class HelpfulVote(BaseModel):
    is_helpful: bool = Field(..., description="Полезен ли ответ")

# Обновляем схемы для разрешения forward references
DiscussionWithAnswersResponse.update_forward_refs()