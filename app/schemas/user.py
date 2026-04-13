from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


# Схемы для аутентификации
class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None


# Схемы для пользователя
class UserBase(BaseModel):
    email: EmailStr
    full_name: str


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    avatar_url: Optional[str] = None
    bio: Optional[str] = None
    location: Optional[str] = None


class UserInDB(UserBase):
    id: int
    hashed_password: str
    avatar_url: Optional[str] = None
    bio: Optional[str] = None
    location: Optional[str] = None
    reputation_score: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class UserResponse(UserBase):
    id: int
    avatar_url: Optional[str] = None
    bio: Optional[str] = None
    location: Optional[str] = None
    reputation_score: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Для совместимости с существующим кодом
class User(UserResponse):
    pass