from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class DiscussionBase(BaseModel):
    title: str = Field(..., max_length=200)
    content: str = Field(..., min_length=10)
    landmark_id: Optional[int] = None
    city: Optional[str] = None


class DiscussionCreate(DiscussionBase):
    pass


class DiscussionUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=200)
    content: Optional[str] = Field(None, min_length=10)
    is_closed: Optional[bool] = None


class DiscussionResponse(DiscussionBase):
    id: int
    user_id: int
    user_name: str
    user_avatar: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    is_closed: bool
    answer_count: int

    class Config:
        from_attributes = True


class AnswerBase(BaseModel):
    content: str = Field(..., min_length=1)


class AnswerCreate(AnswerBase):
    discussion_id: int


class AnswerUpdate(AnswerBase):
    pass


class AnswerResponse(AnswerBase):
    id: int
    user_id: int
    user_name: str
    user_avatar: Optional[str] = None
    discussion_id: int
    created_at: datetime
    updated_at: datetime
    is_helpful: bool
    helpful_votes: int

    class Config:
        from_attributes = True


class VoteCreate(BaseModel):
    is_helpful: bool


# Для совместимости
class Discussion(DiscussionResponse):
    pass