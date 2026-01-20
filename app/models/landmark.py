from sqlalchemy import Column, Integer, String, Float, Text, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

class Landmark(Base):
    __tablename__ = "landmarks"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text)
    city = Column(String(100), nullable=False, index=True)
    country = Column(String(100), nullable=False)
    category = Column(String(100), nullable=False, index=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    address = Column(String(500))
    image_url = Column(String(500))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    favorites = relationship("Favorite", back_populates="landmark", cascade="all, delete-orphan")
    reviews = relationship("Review", back_populates="landmark", cascade="all, delete-orphan")
    
    # Добавляем новую связь для обсуждений
    discussions = relationship("Discussion", back_populates="landmark", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Landmark {self.name} ({self.city})>"