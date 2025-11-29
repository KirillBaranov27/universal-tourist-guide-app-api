from sqlalchemy import Column, Integer, ForeignKey, DateTime, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

class Favorite(Base):
    __tablename__ = "favorites"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    landmark_id = Column(Integer, ForeignKey("landmarks.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Добавляем отношения
    user = relationship("User", back_populates="favorites")
    landmark = relationship("Landmark", back_populates="favorites")

    # Уникальное ограничение: пользователь не может добавить одну достопримечательность дважды
    __table_args__ = (UniqueConstraint('user_id', 'landmark_id', name='unique_user_landmark'),)

    def __repr__(self):
        return f"<Favorite user_id={self.user_id} landmark_id={self.landmark_id}>"