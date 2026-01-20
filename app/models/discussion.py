from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Boolean, Index
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

class Discussion(Base):
    __tablename__ = "discussions"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    
    # Обсуждение может быть привязано к достопримечательности ИЛИ к городу
    landmark_id = Column(Integer, ForeignKey("landmarks.id", ondelete="CASCADE"), nullable=True)
    city = Column(String(100), nullable=True, index=True)  # Если обсуждение о городе в целом
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    is_closed = Column(Boolean, default=False)  # Закрыто ли обсуждение
    
    # Отношения
    user = relationship("User", back_populates="discussions")
    landmark = relationship("Landmark", back_populates="discussions")
    answers = relationship("DiscussionAnswer", back_populates="discussion", cascade="all, delete-orphan")
    
    # Индексы
    __table_args__ = (
        Index('idx_discussion_city_created', 'city', 'created_at'),
        Index('idx_discussion_landmark_created', 'landmark_id', 'created_at'),
    )
    
    def __repr__(self):
        return f"<Discussion {self.title[:30]}...>"


class DiscussionAnswer(Base):
    __tablename__ = "discussion_answers"
    
    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    discussion_id = Column(Integer, ForeignKey("discussions.id", ondelete="CASCADE"), nullable=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    is_helpful = Column(Boolean, default=False)  # Отметка полезного ответа
    helpful_votes = Column(Integer, default=0)  # Количество голосов "полезно"
    
    # Отношения
    user = relationship("User", back_populates="discussion_answers")
    discussion = relationship("Discussion", back_populates="answers")
    
    def __repr__(self):
        return f"<Answer {self.content[:30]}...>"