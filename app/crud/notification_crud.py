<<<<<<< Updated upstream
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
=======
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from app.models.notification import Notification
from app.schemas.notification import NotificationCreate, NotificationUpdate


def get_notification(db: Session, notification_id: int):
    """Получить уведомление по ID"""
    return db.query(Notification).filter(Notification.id == notification_id).first()


def get_user_notifications(
    db: Session, 
    user_id: int, 
    skip: int = 0, 
    limit: int = 50,
    unread_only: bool = False
):
    """Получить уведомления пользователя"""
    query = db.query(Notification).filter(Notification.user_id == user_id)
    
    if unread_only:
        query = query.filter(Notification.is_read == False)
    
    total = query.count()
    notifications = query.order_by(desc(Notification.created_at)).offset(skip).limit(limit).all()
    
    return notifications, total


def get_unread_count(db: Session, user_id: int) -> int:
    """Получить количество непрочитанных уведомлений"""
    return db.query(func.count()).filter(
        Notification.user_id == user_id,
        Notification.is_read == False
    ).scalar()


def create_notification(db: Session, notification: NotificationCreate):
    """Создать новое уведомление"""
    db_notification = Notification(
        user_id=notification.user_id,
        type=notification.type,
        title=notification.title,
        message=notification.message,
        related_id=notification.related_id,
        related_type=notification.related_type
    )
>>>>>>> Stashed changes
    db.add(db_notification)
    db.commit()
    db.refresh(db_notification)
    return db_notification

<<<<<<< Updated upstream
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
=======

def mark_as_read(db: Session, notification_id: int, user_id: int):
    """Отметить уведомление как прочитанное"""
    notification = db.query(Notification).filter(
>>>>>>> Stashed changes
        Notification.id == notification_id,
        Notification.user_id == user_id
    ).first()
    
<<<<<<< Updated upstream
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
=======
    if notification:
        notification.is_read = True
        db.commit()
        db.refresh(notification)
    
    return notification


def mark_all_as_read(db: Session, user_id: int):
    """Отметить все уведомления пользователя как прочитанные"""
    db.query(Notification).filter(
        Notification.user_id == user_id,
        Notification.is_read == False
    ).update({"is_read": True})
    db.commit()
    
    return get_unread_count(db, user_id) == 0


def delete_notification(db: Session, notification_id: int, user_id: int):
    """Удалить уведомление"""
    notification = db.query(Notification).filter(
        Notification.id == notification_id,
        Notification.user_id == user_id
    ).first()
    
    if notification:
        db.delete(notification)
        db.commit()
        return True
    
    return False


# Функции для автоматического создания уведомлений
def create_answer_notification(db: Session, answer_user_id: int, discussion_author_id: int, answer_id: int, discussion_title: str):
    """Создать уведомление о новом ответе на обсуждение"""
    if answer_user_id != discussion_author_id:  # Не уведомляем, если ответил автор обсуждения
        notification = NotificationCreate(
            user_id=discussion_author_id,
            type="new_answer",
            title="Новый ответ на ваше обсуждение",
            message=f"Пользователь ответил на ваше обсуждение '{discussion_title}'",
            related_id=answer_id,
            related_type="answer"
        )
        return create_notification(db, notification)
    return None


def create_like_notification(db: Session, voter_id: int, answer_author_id: int, answer_id: int):
    """Создать уведомление о лайке ответа"""
    if voter_id != answer_author_id:  # Не уведомляем, если лайкнул сам автор
        notification = NotificationCreate(
            user_id=answer_author_id,
            type="answer_liked",
            title="Ваш ответ отметили как полезный",
            message="Кто-то отметил ваш ответ как полезный",
            related_id=answer_id,
            related_type="answer"
        )
        return create_notification(db, notification)
    return None


def create_review_notification(db: Session, review_user_id: int, landmark_owner_id: int, review_id: int, landmark_name: str):
    """Создать уведомление о новом отзыве на достопримечательность (для модераторов/админов)"""
    if review_user_id != landmark_owner_id:
        notification = NotificationCreate(
            user_id=landmark_owner_id,
            type="new_review",
            title="Новый отзыв на достопримечательность",
            message=f"Добавлен новый отзыв на '{landmark_name}'",
            related_id=review_id,
            related_type="review"
        )
        return create_notification(db, notification)
    return None
>>>>>>> Stashed changes
