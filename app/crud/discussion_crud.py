from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_, and_, desc, func
from typing import List, Tuple, Optional
from app.models.discussion import Discussion, DiscussionAnswer
from app.schemas.discussion import DiscussionCreate, DiscussionUpdate, DiscussionAnswerCreate, DiscussionAnswerUpdate
from app.services.notification_service import notification_service

# --- Discussion CRUD ---

def get_discussion(db: Session, discussion_id: int) -> Optional[Discussion]:
    """
    Получить обсуждение по ID
    """
    return db.query(Discussion).options(joinedload(Discussion.user)).filter(Discussion.id == discussion_id).first()

def get_discussions(
    db: Session,
    skip: int = 0,
    limit: int = 50,
    landmark_id: Optional[int] = None,
    city: Optional[str] = None,
    user_id: Optional[int] = None,
    search: Optional[str] = None,
    only_open: bool = False
) -> Tuple[List[Discussion], int]:
    """
    Получить список обсуждений с фильтрами
    """
    query = db.query(Discussion).options(joinedload(Discussion.user))
    
    # Фильтры
    if landmark_id:
        query = query.filter(Discussion.landmark_id == landmark_id)
    if city:
        query = query.filter(Discussion.city == city)
    if user_id:
        query = query.filter(Discussion.user_id == user_id)
    if only_open:
        query = query.filter(Discussion.is_closed == False)
    if search:
        search_filter = or_(
            Discussion.title.ilike(f"%{search}%"),
            Discussion.content.ilike(f"%{search}%")
        )
        query = query.filter(search_filter)
    
    # Сортировка по дате создания (новые сначала)
    query = query.order_by(desc(Discussion.created_at))
    
    # Пагинация
    total = query.count()
    discussions = query.offset(skip).limit(limit).all()
    
    return discussions, total

def create_discussion(db: Session, discussion: DiscussionCreate, user_id: int) -> Discussion:
    """
    Создать новое обсуждение
    """
    db_discussion = Discussion(**discussion.dict(), user_id=user_id)
    db.add(db_discussion)
    db.commit()
    db.refresh(db_discussion)
    return db_discussion

def update_discussion(
    db: Session,
    discussion_id: int,
    discussion: DiscussionUpdate,
    user_id: int
) -> Optional[Discussion]:
    """
    Обновить обсуждение (только автор)
    """
    db_discussion = db.query(Discussion).filter(
        Discussion.id == discussion_id,
        Discussion.user_id == user_id
    ).first()
    
    if not db_discussion:
        return None
    
    update_data = discussion.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_discussion, field, value)
    
    db.commit()
    db.refresh(db_discussion)
    return db_discussion

def delete_discussion(db: Session, discussion_id: int, user_id: int) -> bool:
    """
    Удалить обсуждение (только автор)
    """
    db_discussion = db.query(Discussion).filter(
        Discussion.id == discussion_id,
        Discussion.user_id == user_id
    ).first()
    
    if not db_discussion:
        return False
    
    db.delete(db_discussion)
    db.commit()
    return True

# --- Answer CRUD ---

def get_answer(db: Session, answer_id: int) -> Optional[DiscussionAnswer]:
    """
    Получить ответ по ID
    """
    return db.query(DiscussionAnswer).filter(DiscussionAnswer.id == answer_id).first()

def get_answers_by_discussion(
    db: Session,
    discussion_id: int,
    skip: int = 0,
    limit: int = 100,
    sort_by_helpful: bool = False
) -> Tuple[List[DiscussionAnswer], int]:
    """
    Получить ответы на обсуждение
    """
    query = db.query(DiscussionAnswer).filter(
        DiscussionAnswer.discussion_id == discussion_id
    ).options(joinedload(DiscussionAnswer.user))
    
    # Сортировка
    if sort_by_helpful:
        query = query.order_by(desc(DiscussionAnswer.helpful_votes), desc(DiscussionAnswer.created_at))
    else:
        query = query.order_by(desc(DiscussionAnswer.created_at))
    
    # Пагинация
    total = query.count()
    answers = query.offset(skip).limit(limit).all()
    
    return answers, total

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
        **answer.dict(),
        discussion_id=discussion_id,
        user_id=user_id
    )
    db.add(db_answer)
    db.commit()
    db.refresh(db_answer)
    
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
    
    return db_answer

def update_answer(
    db: Session,
    answer_id: int,
    answer: DiscussionAnswerUpdate,
    user_id: int
) -> Optional[DiscussionAnswer]:
    """
    Обновить ответ (только автор)
    """
    db_answer = db.query(DiscussionAnswer).filter(
        DiscussionAnswer.id == answer_id,
        DiscussionAnswer.user_id == user_id
    ).first()
    
    if not db_answer:
        return None
    
    update_data = answer.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_answer, field, value)
    
    db.commit()
    db.refresh(db_answer)
    return db_answer

def delete_answer(db: Session, answer_id: int, user_id: int) -> bool:
    """
    Удалить ответ (только автор)
    """
    db_answer = db.query(DiscussionAnswer).filter(
        DiscussionAnswer.id == answer_id,
        DiscussionAnswer.user_id == user_id
    ).first()
    
    if not db_answer:
        return False
    
    db.delete(db_answer)
    db.commit()
    return True

def vote_helpful(db: Session, answer_id: int, user_id: int, is_helpful: bool) -> bool:
    """
    Голосовать за полезность ответа
    """
    # TODO: В будущем можно добавить проверку, что пользователь не голосовал уже
    db_answer = db.query(DiscussionAnswer).filter(DiscussionAnswer.id == answer_id).first()
    
    if not db_answer:
        return False
    
    if is_helpful:
        db_answer.helpful_votes += 1
        # Если достигло порога (например, 5 голосов), отмечаем как полезный
        if db_answer.helpful_votes >= 3:
            db_answer.is_helpful = True
    else:
        # Уменьшаем голоса, но не ниже 0
        db_answer.helpful_votes = max(0, db_answer.helpful_votes - 1)
    
    db.commit()
    
    # Обновляем репутацию автора ответа
    update_user_reputation(db, db_answer.user_id, "helpful_answer")
    
    return True

def update_user_reputation(db: Session, user_id: int, action: str):
    """
    Обновить репутацию пользователя за действия
    """
    from app.models.user import User
    db_user = db.query(User).filter(User.id == user_id).first()
    
    if not db_user:
        return
    
    reputation_change = {
        "helpful_answer": 10,  # +10 за полезный ответ
        "created_discussion": 5,  # +5 за создание обсуждения
        "created_answer": 2,  # +2 за ответ
    }
    
    if action in reputation_change:
        db_user.reputation_score += reputation_change[action]
        db.commit()

def get_discussion_stats(db: Session, user_id: int) -> dict:
    """
    Получить статистику по обсуждениям пользователя
    """
    total_discussions = db.query(Discussion).filter(Discussion.user_id == user_id).count()
    total_answers = db.query(DiscussionAnswer).filter(DiscussionAnswer.user_id == user_id).count()
    helpful_answers = db.query(DiscussionAnswer).filter(
        DiscussionAnswer.user_id == user_id,
        DiscussionAnswer.is_helpful == True
    ).count()
    
    return {
        "total_discussions": total_discussions,
        "total_answers": total_answers,
        "helpful_answers": helpful_answers
    }