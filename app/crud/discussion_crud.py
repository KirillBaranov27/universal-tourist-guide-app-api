<<<<<<< Updated upstream
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_, and_, desc, func
from typing import List, Tuple, Optional
from app.models.discussion import Discussion, DiscussionAnswer
from app.schemas.discussion import DiscussionCreate, DiscussionUpdate, DiscussionAnswerCreate, DiscussionAnswerUpdate
from app.services.notification_service import notification_service
=======
from typing import List, Optional, Dict
from sqlalchemy.orm import Session
from sqlalchemy import func, desc, or_
from fastapi import HTTPException
>>>>>>> Stashed changes

# Импортируем модели и схемы
from app import models
from app.schemas import discussion as schemas  # Импортируем схемы для обсуждений


def get_discussion(db: Session, discussion_id: int):
    """Получить обсуждение по ID"""
    return db.query(models.Discussion).filter(models.Discussion.id == discussion_id).first()

<<<<<<< Updated upstream
def get_discussion(db: Session, discussion_id: int) -> Optional[Discussion]:
    """
    Получить обсуждение по ID
    """
    return db.query(Discussion).options(joinedload(Discussion.user)).filter(Discussion.id == discussion_id).first()
=======
>>>>>>> Stashed changes

def get_discussions(
    db: Session,
    skip: int = 0,
    limit: int = 50,
    landmark_id: Optional[int] = None,
    city: Optional[str] = None,
    user_id: Optional[int] = None,
    search: Optional[str] = None,
    only_open: bool = False
):
    """Получить список обсуждений с фильтрами"""
    query = db.query(models.Discussion)
    
    # Применяем фильтры
    if landmark_id:
        query = query.filter(models.Discussion.landmark_id == landmark_id)
    
    if city:
        query = query.filter(models.Discussion.city == city)
    
    if user_id:
        query = query.filter(models.Discussion.user_id == user_id)
    
    if search:
        search_filter = or_(
            models.Discussion.title.ilike(f"%{search}%"),
            models.Discussion.content.ilike(f"%{search}%")
        )
        query = query.filter(search_filter)
    
    if only_open:
        query = query.filter(models.Discussion.is_closed == False)
    
    # Считаем общее количество
    total = query.count()
    
    # Применяем пагинацию и сортировку
    discussions = query.order_by(desc(models.Discussion.created_at)).offset(skip).limit(limit).all()
    
    # Вычисляем количество страниц
    pages = (total + limit - 1) // limit if limit > 0 else 0
    page = skip // limit if limit > 0 else 0
    
    return {
        "items": discussions,
        "total": total,
        "page": page,
        "size": len(discussions),
        "pages": pages
    }


def create_discussion(db: Session, discussion: schemas.DiscussionCreate, user_id: int):
    """Создать новое обсуждение"""
    db_discussion = models.Discussion(
        **discussion.dict(),
        user_id=user_id
    )
    db.add(db_discussion)
    db.commit()
    db.refresh(db_discussion)
    return db_discussion


def update_discussion(db: Session, discussion_id: int, discussion_update: schemas.DiscussionUpdate, user_id: int):
    """Обновить обсуждение"""
    discussion = db.query(models.Discussion).filter(
        models.Discussion.id == discussion_id,
        models.Discussion.user_id == user_id
    ).first()
    
    if not discussion:
        return None
    
    update_data = discussion_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(discussion, field, value)
    
    db.commit()
    db.refresh(discussion)
    return discussion


def delete_discussion(db: Session, discussion_id: int, user_id: int):
    """Удалить обсуждение"""
    discussion = db.query(models.Discussion).filter(
        models.Discussion.id == discussion_id,
        models.Discussion.user_id == user_id
    ).first()
    
    if not discussion:
        return False
    
    db.delete(discussion)
    db.commit()
    return True


def get_discussion_answers(
    db: Session,
    discussion_id: int,
    skip: int = 0,
    limit: int = 50,
    sort_by_helpful: bool = False
):
    """Получить ответы на обсуждение"""
    query = db.query(models.DiscussionAnswer).filter(
        models.DiscussionAnswer.discussion_id == discussion_id
    )
    
    # Применяем сортировку
    if sort_by_helpful:
        query = query.order_by(desc(models.DiscussionAnswer.helpful_votes))
    else:
        query = query.order_by(desc(models.DiscussionAnswer.created_at))
    
    total = query.count()
    answers = query.offset(skip).limit(limit).all()
    
    return {
        "items": answers,
        "total": total
    }

<<<<<<< Updated upstream
def create_answer(
    db: Session,
    answer: DiscussionAnswerCreate,
    discussion_id: int,
    user_id: int
) -> DiscussionAnswer:
    """
    Создать ответ на обсуждение
    """
    # Сначала получаем обсуждение с автором
    discussion = db.query(Discussion).options(
        joinedload(Discussion.user)
    ).filter(Discussion.id == discussion_id).first()
    
    if not discussion:
        raise ValueError("Обсуждение не найдено")
    
    # Создаем ответ
    db_answer = DiscussionAnswer(
=======

def create_answer(db: Session, answer: schemas.AnswerCreate, user_id: int):
    """Создать ответ на обсуждение"""
    # Проверяем, существует ли обсуждение
    discussion = db.query(models.Discussion).filter(
        models.Discussion.id == answer.discussion_id
    ).first()
    
    if not discussion:
        raise HTTPException(status_code=404, detail="Обсуждение не найдено")
    
    db_answer = models.DiscussionAnswer(
>>>>>>> Stashed changes
        **answer.dict(),
        user_id=user_id
    )
    db.add(db_answer)
    db.commit()
    db.refresh(db_answer)
    
<<<<<<< Updated upstream
    # Создаем уведомление для автора обсуждения (если это не он сам отвечает)
    if discussion.user_id != user_id:
        try:
            # Получаем автора ответа
            from app.crud.user_crud import get_user_profile
            answer_author = get_user_profile(db, user_id)
            
            if answer_author:
                notification_service.send_discussion_answer_notification(
                    db=db,
                    discussion_author_id=discussion.user_id,
                    answer_author_name=answer_author.full_name,
                    discussion_title=discussion.title,
                    discussion_id=discussion_id,
                    answer_id=db_answer.id
                )
                print(f"✅ Создано уведомление для пользователя {discussion.user_id} о новом ответе")
        except Exception as e:
            print(f"❌ Ошибка при создании уведомления: {e}")
            # Не прерываем выполнение, если уведомление не создалось
=======
    # Обновляем счетчик ответов в обсуждении
    discussion.answer_count = db.query(func.count()).filter(
        models.DiscussionAnswer.discussion_id == discussion.id
    ).scalar()
    db.commit()
    
    # Создаем уведомление автору обсуждения (если это не сам автор)
    if user_id != discussion.user_id:
        try:
            from app.crud.notification_crud import create_answer_notification
            create_answer_notification(
                db=db,
                answer_user_id=user_id,
                discussion_author_id=discussion.user_id,
                answer_id=db_answer.id,
                discussion_title=discussion.title
            )
        except ImportError:
            # Если модуль уведомлений еще не реализован, просто игнорируем
            pass
>>>>>>> Stashed changes
    
    return db_answer


def update_answer(db: Session, answer_id: int, answer_update: schemas.AnswerUpdate, user_id: int):
    """Обновить ответ"""
    answer = db.query(models.DiscussionAnswer).filter(
        models.DiscussionAnswer.id == answer_id,
        models.DiscussionAnswer.user_id == user_id
    ).first()
    
    if not answer:
        return None
    
    update_data = answer_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(answer, field, value)
    
    db.commit()
    db.refresh(answer)
    return answer


def delete_answer(db: Session, answer_id: int, user_id: int):
    """Удалить ответ"""
    answer = db.query(models.DiscussionAnswer).filter(
        models.DiscussionAnswer.id == answer_id,
        models.DiscussionAnswer.user_id == user_id
    ).first()
    
    if not answer:
        return False
    
    # Обновляем счетчик ответов в обсуждении
    discussion = answer.discussion
    db.delete(answer)
    db.commit()
    
    # Обновляем счетчик
    if discussion:
        discussion.answer_count = db.query(func.count()).filter(
            models.DiscussionAnswer.discussion_id == discussion.id
        ).scalar()
        db.commit()
    
    return True


def vote_for_answer(db: Session, answer_id: int, vote: schemas.VoteCreate, user_id: int):
    """Голосовать за полезность ответа"""
    answer = db.query(models.DiscussionAnswer).filter(
        models.DiscussionAnswer.id == answer_id
    ).first()
    
    if not answer:
        raise HTTPException(status_code=404, detail="Ответ не найден")
    
    # Проверяем, не голосовал ли уже пользователь
    # (в реальном приложении нужно хранить таблицу голосов)
    # Здесь упрощенная логика
    
    if vote.is_helpful:
        answer.helpful_votes += 1
        # Если ответ получил 3+ голосов полезности, отмечаем его
        if answer.helpful_votes >= 3:
            answer.is_helpful = True
        
        # Создаем уведомление автору ответа (если это не сам голосующий)
        if user_id != answer.user_id:
            try:
                from app.crud.notification_crud import create_like_notification
                create_like_notification(
                    db=db,
                    voter_id=user_id,
                    answer_author_id=answer.user_id,
                    answer_id=answer_id
                )
            except ImportError:
                # Если модуль уведомлений еще не реализован, просто игнорируем
                pass
    else:
        # Уменьшаем голоса (но не ниже 0)
        answer.helpful_votes = max(0, answer.helpful_votes - 1)
        if answer.helpful_votes < 3:
            answer.is_helpful = False
    
    db.commit()
    db.refresh(answer)
    
    # Обновляем репутацию пользователя, чей ответ получил голос
    if vote.is_helpful and user_id != answer.user_id:
        user = db.query(models.User).filter(models.User.id == answer.user_id).first()
        if user:
            user.reputation_score += 5  # +5 к репутации за полезный ответ
            db.commit()
    
    return answer

def get_discussion_stats(db: Session, user_id: int) -> dict:
    """
    Получить статистику пользователя по обсуждениям и ответам
    """
    from sqlalchemy import func
    
    total_discussions = db.query(func.count()).filter(
        models.Discussion.user_id == user_id
    ).scalar() or 0
    
    total_answers = db.query(func.count()).filter(
        models.DiscussionAnswer.user_id == user_id
    ).scalar() or 0
    
    helpful_answers = db.query(func.count()).filter(
        models.DiscussionAnswer.user_id == user_id,
        models.DiscussionAnswer.is_helpful == True
    ).scalar() or 0
    
    return {
        "total_discussions": total_discussions,
        "total_answers": total_answers,
        "helpful_answers": helpful_answers
    }