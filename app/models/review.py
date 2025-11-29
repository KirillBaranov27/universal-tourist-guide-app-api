from sqlalchemy import Column, Integer, ForeignKey, Text, Float, DateTime, UniqueConstraint, CheckConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    landmark_id = Column(Integer, ForeignKey("landmarks.id", ondelete="CASCADE"), nullable=False)
    rating = Column(Float, nullable=False)  # Оценка от 1 до 5
    comment = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Добавляем отношения
    user = relationship("User", back_populates="reviews")
    landmark = relationship("Landmark", back_populates="reviews")

    # Уникальное ограничение: один пользователь - один отзыв на достопримечательность
    __table_args__ = (
        UniqueConstraint('user_id', 'landmark_id', name='unique_user_landmark_review'),
        CheckConstraint('rating >= 1 AND rating <= 5', name='rating_range_check')
    )

    def __repr__(self):
        return f"<Review user_id={self.user_id} landmark_id={self.landmark_id} rating={self.rating}>"