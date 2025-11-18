from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import create_access_token, verify_password, get_password_hash
from app.schemas.user import UserCreate, UserLogin, Token, UserResponse
from app.models.user import User as UserModel
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/register", response_model=UserResponse)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """
    Регистрация нового пользователя
    """
    try:
        logger.info(f"Попытка регистрации пользователя: {user_data.email}")
        
        # Проверяем существует ли пользователь
        db_user = db.query(UserModel).filter(UserModel.email == user_data.email).first()
        if db_user:
            logger.warning(f"Пользователь с email {user_data.email} уже существует")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email уже зарегистрирован"
            )
        
        # Создаем нового пользователя
        logger.info(f"Хэшируем пароль для {user_data.email}")
        hashed_password = get_password_hash(user_data.password)
        logger.info(f"Пароль успешно хэширован")
        
        db_user = UserModel(
            email=user_data.email,
            hashed_password=hashed_password,
            full_name=user_data.full_name
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        
        logger.info(f"Пользователь {user_data.email} успешно зарегистрирован")
        return db_user
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Ошибка при регистрации: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка сервера: {str(e)}"
        )

@router.post("/login", response_model=Token)
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    """
    Аутентификация пользователя
    """
    try:
        logger.info(f"Попытка входа пользователя: {user_data.email}")
        
        db_user = db.query(UserModel).filter(UserModel.email == user_data.email).first()
        if not db_user:
            logger.warning(f"Пользователь {user_data.email} не найден")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Неверный email или пароль"
            )
        
        logger.info(f"Проверяем пароль для {user_data.email}")
        if not verify_password(user_data.password, db_user.hashed_password):
            logger.warning(f"Неверный пароль для пользователя {user_data.email}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Неверный email или пароль"
            )
        
        access_token = create_access_token(subject=db_user.email)
        logger.info(f"Успешный вход пользователя {user_data.email}")
        return {"access_token": access_token, "token_type": "bearer"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Ошибка при входе: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ошибка сервера при аутентификации"
        )