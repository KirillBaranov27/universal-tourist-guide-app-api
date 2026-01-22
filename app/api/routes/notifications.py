from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.api.dependencies import get_current_user
from app.models.user import User
from app.schemas.notification import (
    NotificationResponse,
    NotificationListResponse,
    NotificationStatsResponse,
    MarkAsReadRequest,
    MarkAsReadResponse
)
from app.crud.notification_crud import (
    get_user_notifications,
    create_system_notification,
    mark_as_read,
    mark_as_archived,
    delete_notification,
    delete_all_read_notifications,
    get_notification_stats
)

router = APIRouter()

# --- Получение уведомлений ---

@router.get("/notifications", response_model=NotificationListResponse)
def read_user_notifications(
    skip: int = Query(0, ge=0, description="Смещение для пагинации"),
    limit: int = Query(50, ge=1, le=100, description="Лимит записей"),
    only_unread: bool = Query(False, description="Только непрочитанные"),
    include_archived: bool = Query(False, description="Включая архивированные"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Получить уведомления пользователя
    """
    notifications, total, unread_count = get_user_notifications(
        db,
        user_id=current_user.id,
        skip=skip,
        limit=limit,
        only_unread=only_unread,
        include_archived=include_archived
    )
    
    items = []
    for notification in notifications:
        items.append(NotificationResponse(
            id=notification.id,
            user_id=notification.user_id,
            notification_type=notification.notification_type,
            title=notification.title,
            message=notification.message,
            data=notification.data,
            is_read=notification.is_read,
            is_archived=notification.is_archived,
            created_at=notification.created_at,
            read_at=notification.read_at
        ))
    
    return NotificationListResponse(
        items=items,
        total=total,
        unread_count=unread_count
    )

@router.get("/notifications/stats", response_model=NotificationStatsResponse)
def get_notifications_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Получить статистику по уведомлениям
    """
    stats = get_notification_stats(db, current_user.id)
    return NotificationStatsResponse(**stats)

# --- Управление уведомлениями ---

@router.post("/notifications/mark-read", response_model=MarkAsReadResponse)
def mark_notifications_as_read(
    request: MarkAsReadRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Отметить уведомления как прочитанные
    """
    if request.all_unread:
        updated_count = mark_as_read(db, current_user.id)
    elif request.notification_ids:
        updated_count = mark_as_read(db, current_user.id, request.notification_ids)
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Укажите notification_ids или установите all_unread=True"
        )
    
    return MarkAsReadResponse(updated_count=updated_count)

@router.post("/notifications/{notification_id}/read")
def mark_single_as_read(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Отметить одно уведомление как прочитанное
    """
    updated_count = mark_as_read(db, current_user.id, [notification_id])
    
    if updated_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Уведомление не найдено или уже прочитано"
        )
    
    return {"message": "Уведомление отмечено как прочитанное"}

@router.post("/notifications/archive")
def archive_notifications(
    notification_ids: List[int],
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Архивировать уведомления
    """
    updated_count = mark_as_archived(db, current_user.id, notification_ids)
    
    return {"message": f"Уведомлений архивировано: {updated_count}"}

@router.delete("/notifications/{notification_id}")
def delete_user_notification(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Удалить уведомление
    """
    success = delete_notification(db, notification_id, current_user.id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Уведомление не найдено"
        )
    
    return {"message": "Уведомление удалено"}

@router.delete("/notifications/cleanup/read")
def cleanup_read_notifications(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Удалить все прочитанные уведомления
    """
    deleted_count = delete_all_read_notifications(db, current_user.id)
    
    return {"message": f"Удалено {deleted_count} прочитанных уведомлений"}

# --- Системные уведомления (для внутреннего использования) ---

@router.post("/notifications/test")
def send_test_notification(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Отправить тестовое уведомление (для разработки)
    """
    notification = create_system_notification(
        db=db,
        user_id=current_user.id,
        notification_type="system",
        title="Тестовое уведомление",
        message="Это тестовое уведомление для проверки системы",
        data={"test": True, "timestamp": "now"}
    )
    
    return {
        "message": "Тестовое уведомление отправлено",
        "notification_id": notification.id
    }
