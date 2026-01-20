from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional, List

from app.core.database import get_db
from app.api.dependencies import get_current_user
from app.models.user import User
from app.models.landmark import Landmark
from app.schemas.discussion import (
    DiscussionCreate, 
    DiscussionUpdate, 
    DiscussionResponse,
    DiscussionWithAnswersResponse,
    DiscussionListResponse,
    DiscussionAnswerCreate,
    DiscussionAnswerUpdate,
    DiscussionAnswerResponse,
    AnswerListResponse,
    HelpfulVote
)
from app.crud.discussion_crud import (
    get_discussion,
    get_discussions,
    create_discussion,
    update_discussion,
    delete_discussion,
    get_answers_by_discussion,
    create_answer,
    update_answer,
    delete_answer,
    vote_helpful
)

router = APIRouter()

# --- Обсуждения ---

@router.get("/discussions", response_model=DiscussionListResponse)
def read_discussions(
    skip: int = Query(0, ge=0, description="Смещение для пагинации"),
    limit: int = Query(50, ge=1, le=100, description="Лимит записей"),
    landmark_id: Optional[int] = Query(None, description="Фильтр по достопримечательности"),
    city: Optional[str] = Query(None, description="Фильтр по городу"),
    user_id: Optional[int] = Query(None, description="Фильтр по пользователю"),
    search: Optional[str] = Query(None, description="Поиск по заголовку и содержанию"),
    only_open: bool = Query(False, description="Только открытые обсуждения"),
    db: Session = Depends(get_db)
):
    """
    Получить список обсуждений с фильтрами
    """
    discussions, total = get_discussions(
        db,
        skip=skip,
        limit=limit,
        landmark_id=landmark_id,
        city=city,
        user_id=user_id,
        search=search,
        only_open=only_open
    )
    
    # Преобразуем в ответ
    items = []
    for discussion in discussions:
        items.append(DiscussionResponse(
            id=discussion.id,
            title=discussion.title,
            content=discussion.content,
            user_id=discussion.user_id,
            user_name=discussion.user.full_name,
            user_avatar=discussion.user.avatar_url,
            landmark_id=discussion.landmark_id,
            city=discussion.city,
            created_at=discussion.created_at,
            updated_at=discussion.updated_at,
            is_closed=discussion.is_closed,
            answer_count=len(discussion.answers)
        ))
    
    # Рассчитываем пагинацию
    pages = (total + limit - 1) // limit if limit > 0 else 1
    current_page = (skip // limit) + 1 if limit > 0 else 1
    
    return DiscussionListResponse(
        items=items,
        total=total,
        page=current_page,
        size=limit,
        pages=pages
    )

@router.get("/discussions/{discussion_id}", response_model=DiscussionWithAnswersResponse)
def read_discussion(
    discussion_id: int,
    db: Session = Depends(get_db)
):
    """
    Получить обсуждение с ответами
    """
    discussion = get_discussion(db, discussion_id)
    if not discussion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Обсуждение не найдено"
        )
    
    # Получаем ответы
    answers, _ = get_answers_by_discussion(db, discussion_id, sort_by_helpful=True)
    
    # Формируем ответы
    answer_items = []
    for answer in answers:
        answer_items.append(DiscussionAnswerResponse(
            id=answer.id,
            content=answer.content,
            user_id=answer.user_id,
            user_name=answer.user.full_name,
            user_avatar=answer.user.avatar_url,
            discussion_id=answer.discussion_id,
            created_at=answer.created_at,
            updated_at=answer.updated_at,
            is_helpful=answer.is_helpful,
            helpful_votes=answer.helpful_votes
        ))
    
    return DiscussionWithAnswersResponse(
        id=discussion.id,
        title=discussion.title,
        content=discussion.content,
        user_id=discussion.user_id,
        user_name=discussion.user.full_name,
        user_avatar=discussion.user.avatar_url,
        landmark_id=discussion.landmark_id,
        city=discussion.city,
        created_at=discussion.created_at,
        updated_at=discussion.updated_at,
        is_closed=discussion.is_closed,
        answer_count=len(discussion.answers),
        answers=answer_items
    )

@router.post("/discussions", response_model=DiscussionResponse)
def create_new_discussion(
    discussion: DiscussionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Создать новое обсуждение
    """
    # Проверяем, если привязано к достопримечательности, что она существует
    if discussion.landmark_id:
        landmark = db.query(Landmark).filter(Landmark.id == discussion.landmark_id).first()
        if not landmark:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Достопримечательность не найдена"
            )
    
    db_discussion = create_discussion(db=db, discussion=discussion, user_id=current_user.id)
    
    return DiscussionResponse(
        id=db_discussion.id,
        title=db_discussion.title,
        content=db_discussion.content,
        user_id=db_discussion.user_id,
        user_name=current_user.full_name,
        user_avatar=current_user.avatar_url,
        landmark_id=db_discussion.landmark_id,
        city=db_discussion.city,
        created_at=db_discussion.created_at,
        updated_at=db_discussion.updated_at,
        is_closed=db_discussion.is_closed,
        answer_count=0
    )

@router.put("/discussions/{discussion_id}", response_model=DiscussionResponse)
def update_existing_discussion(
    discussion_id: int,
    discussion: DiscussionUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Обновить обсуждение
    """
    db_discussion = update_discussion(
        db, discussion_id=discussion_id, discussion=discussion, user_id=current_user.id
    )
    
    if db_discussion is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Обсуждение не найдено или у вас нет прав"
        )
    
    return DiscussionResponse(
        id=db_discussion.id,
        title=db_discussion.title,
        content=db_discussion.content,
        user_id=db_discussion.user_id,
        user_name=current_user.full_name,
        user_avatar=current_user.avatar_url,
        landmark_id=db_discussion.landmark_id,
        city=db_discussion.city,
        created_at=db_discussion.created_at,
        updated_at=db_discussion.updated_at,
        is_closed=db_discussion.is_closed,
        answer_count=len(db_discussion.answers)
    )

@router.delete("/discussions/{discussion_id}")
def delete_existing_discussion(
    discussion_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Удалить обсуждение
    """
    success = delete_discussion(db, discussion_id=discussion_id, user_id=current_user.id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Обсуждение не найдено или у вас нет прав"
        )
    
    return {"message": "Обсуждение успешно удалено"}

# --- Ответы ---

@router.get("/discussions/{discussion_id}/answers", response_model=AnswerListResponse)
def read_discussion_answers(
    discussion_id: int,
    skip: int = Query(0, ge=0, description="Смещение для пагинации"),
    limit: int = Query(50, ge=1, le=100, description="Лимит записей"),
    sort_by_helpful: bool = Query(False, description="Сортировать по полезности"),
    db: Session = Depends(get_db)
):
    """
    Получить ответы на обсуждение
    """
    # Проверяем существование обсуждения
    discussion = get_discussion(db, discussion_id)
    if not discussion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Обсуждение не найдено"
        )
    
    answers, total = get_answers_by_discussion(
        db, discussion_id, skip=skip, limit=limit, sort_by_helpful=sort_by_helpful
    )
    
    # Преобразуем в ответ
    items = []
    for answer in answers:
        items.append(DiscussionAnswerResponse(
            id=answer.id,
            content=answer.content,
            user_id=answer.user_id,
            user_name=answer.user.full_name,
            user_avatar=answer.user.avatar_url,
            discussion_id=answer.discussion_id,
            created_at=answer.created_at,
            updated_at=answer.updated_at,
            is_helpful=answer.is_helpful,
            helpful_votes=answer.helpful_votes
        ))
    
    return AnswerListResponse(items=items, total=total)

@router.post("/discussions/{discussion_id}/answers", response_model=DiscussionAnswerResponse)
def create_new_answer(
    discussion_id: int,
    answer: DiscussionAnswerCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Создать ответ на обсуждение
    """
    # Проверяем существование обсуждения
    discussion = get_discussion(db, discussion_id)
    if not discussion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Обсуждение не найдено"
        )
    
    # Проверяем, не закрыто ли обсуждение
    if discussion.is_closed:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Обсуждение закрыто для новых ответов"
        )
    
    db_answer = create_answer(
        db=db, answer=answer, discussion_id=discussion_id, user_id=current_user.id
    )
    
    return DiscussionAnswerResponse(
        id=db_answer.id,
        content=db_answer.content,
        user_id=db_answer.user_id,
        user_name=current_user.full_name,
        user_avatar=current_user.avatar_url,
        discussion_id=db_answer.discussion_id,
        created_at=db_answer.created_at,
        updated_at=db_answer.updated_at,
        is_helpful=db_answer.is_helpful,
        helpful_votes=db_answer.helpful_votes
    )

@router.put("/discussions/answers/{answer_id}", response_model=DiscussionAnswerResponse)
def update_existing_answer(
    answer_id: int,
    answer: DiscussionAnswerUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Обновить ответ
    """
    db_answer = update_answer(db, answer_id=answer_id, answer=answer, user_id=current_user.id)
    
    if db_answer is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ответ не найден или у вас нет прав"
        )
    
    return DiscussionAnswerResponse(
        id=db_answer.id,
        content=db_answer.content,
        user_id=db_answer.user_id,
        user_name=current_user.full_name,
        user_avatar=current_user.avatar_url,
        discussion_id=db_answer.discussion_id,
        created_at=db_answer.created_at,
        updated_at=db_answer.updated_at,
        is_helpful=db_answer.is_helpful,
        helpful_votes=db_answer.helpful_votes
    )

@router.delete("/discussions/answers/{answer_id}")
def delete_existing_answer(
    answer_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Удалить ответ
    """
    success = delete_answer(db, answer_id=answer_id, user_id=current_user.id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ответ не найден или у вас нет прав"
        )
    
    return {"message": "Ответ успешно удален"}

@router.post("/discussions/answers/{answer_id}/vote")
def vote_for_answer(
    answer_id: int,
    vote: HelpfulVote,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Голосовать за полезность ответа
    """
    success = vote_helpful(db, answer_id=answer_id, user_id=current_user.id, is_helpful=vote.is_helpful)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ответ не найден"
        )
    
    return {"message": "Голос учтен"}