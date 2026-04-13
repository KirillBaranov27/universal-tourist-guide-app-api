<<<<<<< Updated upstream
from pydantic import BaseModel, ConfigDict, Field
from typing import Optional, Dict, Any, List
from datetime import datetime

class NotificationBase(BaseModel):
    notification_type: str = Field(..., min_length=1, max_length=50, description="Тип уведомления")
    title: str = Field(..., min_length=1, max_length=200, description="Заголовок уведомления")
    message: str = Field(..., min_length=1, description="Текст уведомления")
    data: Optional[Dict[str, Any]] = Field(None, description="Дополнительные данные")
=======
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


class NotificationType(str, Enum):
    NEW_ANSWER = "new_answer"
    ANSWER_LIKED = "answer_liked"
    NEW_REVIEW = "new_review"
    NEW_DISCUSSION = "new_discussion"
    SYSTEM = "system"


class NotificationBase(BaseModel):
    type: NotificationType
    title: str = Field(..., max_length=200)
    message: str
    related_id: Optional[int] = None
    related_type: Optional[str] = None

>>>>>>> Stashed changes

class NotificationCreate(NotificationBase):
    user_id: int

<<<<<<< Updated upstream
class NotificationUpdate(BaseModel):
    is_read: Optional[bool] = None
    is_archived: Optional[bool] = None

class NotificationResponse(NotificationBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    user_id: int
    is_read: bool
    is_archived: bool
    created_at: datetime
    read_at: Optional[datetime] = None
=======

class NotificationUpdate(BaseModel):
    is_read: Optional[bool] = None


class NotificationResponse(NotificationBase):
    id: int
    user_id: int
    is_read: bool
    created_at: datetime

    class Config:
        from_attributes = True


class UnreadCountResponse(BaseModel):
    count: int

>>>>>>> Stashed changes

class NotificationListResponse(BaseModel):
    items: List[NotificationResponse]
    total: int
<<<<<<< Updated upstream
    unread_count: int

class NotificationStatsResponse(BaseModel):
    total: int
    unread: int
    read: int
    archived: int

class MarkAsReadRequest(BaseModel):
    notification_ids: Optional[List[int]] = Field(None, description="Список ID уведомлений для отметки как прочитанные")
    all_unread: Optional[bool] = Field(False, description="Отметить все непрочитанные как прочитанные")

class MarkAsReadResponse(BaseModel):
    updated_count: int
=======
    unread_count: int
>>>>>>> Stashed changes
