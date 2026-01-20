from sqlalchemy import Column, String, Text, Integer, Float, DateTime, ForeignKey, Table, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class CityProfile(Base):
    __tablename__ = "city_profiles"
    
    city_name = Column(String(100), primary_key=True, index=True)
    country = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    image_url = Column(String(500), nullable=True)
    total_landmarks = Column(Integer, default=0, nullable=False)
    total_reviews = Column(Integer, default=0, nullable=False)
    total_discussions = Column(Integer, default=0, nullable=False)
    average_rating = Column(Float, default=0.0, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    

    # landmarks = relationship("Landmark", back_populates="city_profile")
    
    def __repr__(self):
        return f"<CityProfile {self.city_name}, {self.country}>"


# Таблица для хранения популярных категорий по городам (для кэширования)
class CityCategoryStats(Base):
    __tablename__ = "city_category_stats"
    
    id = Column(Integer, primary_key=True, index=True)
    city_name = Column(String(100), nullable=False, index=True)
    category = Column(String(100), nullable=False, index=True)
    count = Column(Integer, default=0, nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Уникальное ограничение: одна категория на город
    __table_args__ = (
        UniqueConstraint('city_name', 'category', name='unique_city_category'),
    )
    
    def __repr__(self):
        return f"<CityCategoryStats {self.city_name} - {self.category}: {self.count}>"