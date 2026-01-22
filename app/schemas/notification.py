from pydantic import BaseModel, ConfigDict, Field
from typing import Optional, Dict, Any, List
from datetime import datetime

class NotificationBase(BaseModel):
    notification_type: str = Field(..., min_length=1, max_length=50, description="Тип уведомления")
    title: str = Field(..., min_length=1, max_length=200, description="Заголовок уведомления")
    message: str = Field(..., min_length=1, description="Текст уведомления")
    data: Optional[Dict[str, Any]] = Field(None, description="Дополнительные данные")

class NotificationCreate(NotificationBase):
    user_id: int

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

class NotificationListResponse(BaseModel):
    items: List[NotificationResponse]
    total: int
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
