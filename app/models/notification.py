<<<<<<< Updated upstream
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Boolean, JSON
=======
from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, DateTime
>>>>>>> Stashed changes
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

<<<<<<< Updated upstream
=======

>>>>>>> Stashed changes
class Notification(Base):
    __tablename__ = "notifications"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
<<<<<<< Updated upstream
    
    # Тип уведомления
    notification_type = Column(String(50), nullable=False, index=True)
    
    # Заголовок и содержание
    title = Column(String(200), nullable=False)
    message = Column(Text, nullable=False)
    
    # Данные для навигации/действий
    data = Column(JSON, nullable=True)  # JSON с дополнительными данными
    
    # Статус
    is_read = Column(Boolean, default=False, nullable=False)
    is_archived = Column(Boolean, default=False, nullable=False)
    
    # Даты
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    read_at = Column(DateTime(timezone=True), nullable=True)
    
    # Связи
    user = relationship("User", back_populates="notifications")
    
    def __repr__(self):
        return f"<Notification {self.id} for user {self.user_id}>"
=======
    type = Column(String(50), nullable=False, index=True)  # new_answer, answer_liked, etc.
    title = Column(String(200), nullable=False)
    message = Column(Text, nullable=False)
    related_id = Column(Integer, nullable=True)  # ID связанной сущности
    related_type = Column(String(50), nullable=True)  # Тип сущности: discussion, answer, review
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Отношения
    user = relationship("User", back_populates="notifications")
    
    def __repr__(self):
        return f"<Notification {self.type} for user {self.user_id}>"
>>>>>>> Stashed changes
