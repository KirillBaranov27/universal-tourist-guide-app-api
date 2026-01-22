from sqlalchemy.orm import Session
from typing import List, Tuple, Optional, Dict, Any
from sqlalchemy import desc
from app.models.notification import Notification
from app.schemas.notification import NotificationCreate, NotificationUpdate

def get_notification(db: Session, notification_id: int) -> Optional[Notification]:
    """Получить уведомление по ID"""
    return db.query(Notification).filter(Notification.id == notification_id).first()

def get_user_notifications(
    db: Session,
    user_id: int,
    skip: int = 0,
    limit: int = 50,
    only_unread: bool = False,
    include_archived: bool = False
) -> Tuple[List[Notification], int, int]:
    """Получить уведомления пользователя"""
    query = db.query(Notification).filter(Notification.user_id == user_id)
    
    if only_unread:
        query = query.filter(Notification.is_read == False)
    
    if not include_archived:
        query = query.filter(Notification.is_archived == False)
    
    # Получаем общее количество
    total = query.count()
    
    # Получаем количество непрочитанных
    unread_count = db.query(Notification).filter(
        Notification.user_id == user_id,
        Notification.is_read == False,
        Notification.is_archived == False
    ).count()
    
    # Применяем сортировку (новые сначала) и пагинацию
    notifications = query.order_by(desc(Notification.created_at))\
                        .offset(skip)\
                        .limit(limit)\
                        .all()
    
    return notifications, total, unread_count

def create_notification(db: Session, notification: NotificationCreate) -> Notification:
    """Создать новое уведомление"""
    db_notification = Notification(**notification.dict())
    db.add(db_notification)
    db.commit()
    db.refresh(db_notification)
    return db_notification

def create_system_notification(
    db: Session,
    user_id: int,
    notification_type: str,
    title: str,
    message: str,
    data: Optional[Dict[str, Any]] = None
) -> Notification:
    """Создать системное уведомление (вспомогательный метод)"""
    notification = NotificationCreate(
        user_id=user_id,
        notification_type=notification_type,
        title=title,
        message=message,
        data=data
    )
    return create_notification(db, notification)

def mark_as_read(db: Session, user_id: int, notification_ids: Optional[List[int]] = None) -> int:
    """Отметить уведомления как прочитанные"""
    from sqlalchemy import func
    
    query = db.query(Notification).filter(
        Notification.user_id == user_id,
        Notification.is_read == False
    )
    
    if notification_ids:
        query = query.filter(Notification.id.in_(notification_ids))
    
    # Обновляем
    updated_count = query.update(
        {"is_read": True, "read_at": func.now()},
        synchronize_session=False
    )
    db.commit()
    
    return updated_count

def mark_as_archived(db: Session, user_id: int, notification_ids: List[int]) -> int:
    """Отметить уведомления как архивированные"""
    updated_count = db.query(Notification).filter(
        Notification.user_id == user_id,
        Notification.id.in_(notification_ids)
    ).update({"is_archived": True}, synchronize_session=False)
    
    db.commit()
    return updated_count

def delete_notification(db: Session, notification_id: int, user_id: int) -> bool:
    """Удалить уведомление"""
    db_notification = db.query(Notification).filter(
        Notification.id == notification_id,
        Notification.user_id == user_id
    ).first()
    
    if not db_notification:
        return False
    
    db.delete(db_notification)
    db.commit()
    return True

def delete_all_read_notifications(db: Session, user_id: int) -> int:
    """Удалить все прочитанные уведомления"""
    deleted_count = db.query(Notification).filter(
        Notification.user_id == user_id,
        Notification.is_read == True
    ).delete(synchronize_session=False)
    
    db.commit()
    return deleted_count

def get_notification_stats(db: Session, user_id: int) -> Dict[str, int]:
    """Получить статистику по уведомлениям пользователя"""
    total = db.query(Notification).filter(Notification.user_id == user_id).count()
    unread = db.query(Notification).filter(
        Notification.user_id == user_id,
        Notification.is_read == False
    ).count()
    read = total - unread
    archived = db.query(Notification).filter(
        Notification.user_id == user_id,
        Notification.is_archived == True
    ).count()
    
    return {
        "total": total,
        "unread": unread,
        "read": read,
        "archived": archived
    }
