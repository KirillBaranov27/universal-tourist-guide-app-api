"""
Сервис для создания уведомлений при различных событиях в системе
"""
from sqlalchemy.orm import Session
from typing import Optional, Dict, Any
from app.crud.notification_crud import create_system_notification

class NotificationService:
    """Сервис уведомлений"""
    
    @staticmethod
    def send_discussion_answer_notification(
        db: Session,
        discussion_author_id: int,
        answer_author_name: str,
        discussion_title: str,
        discussion_id: int,
        answer_id: int
    ):
        """Уведомление при ответе на обсуждение"""
        try:
            notification = create_system_notification(
                db=db,
                user_id=discussion_author_id,
                notification_type="discussion_answer",
                title="🎯 Новый ответ на ваше обсуждение",
                message=f"👤 Пользователь {answer_author_name} ответил на ваше обсуждение '{discussion_title}'",
                data={
                    "discussion_id": discussion_id,
                    "answer_id": answer_id,
                    "action": "view_discussion",
                    "notification_type": "discussion_answer"
                }
            )
            print(f"📬 Уведомление создано: ID={notification.id}, для пользователя={discussion_author_id}")
            return notification
        except Exception as e:
            print(f"❌ Ошибка при создании уведомления: {e}")
            return None
    
    @staticmethod
    def send_discussion_reply_notification(
        db: Session,
        original_answer_author_id: int,
        replier_name: str,
        discussion_title: str,
        discussion_id: int,
        reply_id: int
    ):
        """Уведомление при ответе на ответ в обсуждении"""
        return create_system_notification(
            db=db,
            user_id=original_answer_author_id,
            notification_type="discussion_reply",
            title="↪️ Ответ на ваш ответ",
            message=f"👤 Пользователь {replier_name} ответил на ваш комментарий в обсуждении '{discussion_title}'",
            data={
                "discussion_id": discussion_id,
                "reply_id": reply_id,
                "action": "view_discussion",
                "notification_type": "discussion_reply"
            }
        )
    
    @staticmethod
    def send_new_discussion_notification(
        db: Session,
        city: str,
        landmark_name: str,
        discussion_title: str,
        discussion_id: int,
        user_ids: list  # ID пользователей, которые следят за городом/достопримечательностью
    ):
        """Уведомление о новом обсуждении в городе/достопримечательности"""
        notifications = []
        for user_id in user_ids:
            notification = create_system_notification(
                db=db,
                user_id=user_id,
                notification_type="new_discussion",
                title="💬 Новое обсуждение",
                message=f"📝 Новое обсуждение '{discussion_title}' в {city}{' - ' + landmark_name if landmark_name else ''}",
                data={
                    "discussion_id": discussion_id,
                    "city": city,
                    "landmark_name": landmark_name,
                    "action": "view_discussion",
                    "notification_type": "new_discussion"
                }
            )
            notifications.append(notification)
        return notifications
    
    @staticmethod
    def send_landmark_review_notification(
        db: Session,
        landmark_author_id: int,  # ID автора достопримечательности (если есть)
        reviewer_name: str,
        landmark_name: str,
        landmark_id: int,
        review_id: int,
        rating: float
    ):
        """Уведомление при новом отзыве о достопримечательности"""
        if landmark_author_id:
            return create_system_notification(
                db=db,
                user_id=landmark_author_id,
                notification_type="landmark_review",
                title="⭐ Новый отзыв",
                message=f"👤 Пользователь {reviewer_name} оставил отзыв ({rating}/5) на вашу достопримечательность '{landmark_name}'",
                data={
                    "landmark_id": landmark_id,
                    "review_id": review_id,
                    "rating": rating,
                    "action": "view_reviews",
                    "notification_type": "landmark_review"
                }
            )
        return None
    
    @staticmethod
    def send_review_reply_notification(
        db: Session,
        review_author_id: int,
        replier_name: str,
        landmark_name: str,
        landmark_id: int,
        review_id: int
    ):
        """Уведомление при ответе на отзыв"""
        return create_system_notification(
            db=db,
            user_id=review_author_id,
            notification_type="review_reply",
            title="💬 Ответ на ваш отзыв",
            message=f"👤 Пользователь {replier_name} ответил на ваш отзыв о '{landmark_name}'",
            data={
                "landmark_id": landmark_id,
                "review_id": review_id,
                "action": "view_reviews",
                "notification_type": "review_reply"
            }
        )
    
    @staticmethod
    def send_new_follower_notification(
        db: Session,
        user_id: int,
        follower_name: str,
        follower_id: int
    ):
        """Уведомление о новом подписчике"""
        return create_system_notification(
            db=db,
            user_id=user_id,
            notification_type="new_follower",
            title="👥 Новый подписчик",
            message=f"👤 Пользователь {follower_name} подписался на вас",
            data={
                "follower_id": follower_id,
                "action": "view_profile",
                "notification_type": "new_follower"
            }
        )
    
    @staticmethod
    def send_welcome_notification(
        db: Session,
        user_id: int,
        user_name: str
    ):
        """Приветственное уведомление для нового пользователя"""
        return create_system_notification(
            db=db,
            user_id=user_id,
            notification_type="welcome",
            title=f"🎉 Добро пожаловать, {user_name}!",
            message="Спасибо за регистрацию в Universal Tourist Guide! Исследуйте достопримечательности, оставляйте отзывы и общайтесь с другими путешественниками.",
            data={
                "action": "explore",
                "welcome_tour": True,
                "notification_type": "welcome"
            }
        )
    
    @staticmethod
    def send_system_notification(
        db: Session,
        user_id: int,
        title: str,
        message: str,
        data: Optional[Dict[str, Any]] = None
    ):
        """Отправить системное уведомление"""
        return create_system_notification(
            db=db,
            user_id=user_id,
            notification_type="system",
            title=title,
            message=message,
            data=data or {}
        )

# Глобальный экземпляр сервиса
notification_service = NotificationService()