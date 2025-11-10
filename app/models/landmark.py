from sqlalchemy import Column, Integer, String, Float, Text, DateTime
from sqlalchemy.sql import func
from app.core.database import Base

class Landmark(Base):
    """Модель достопримечательности"""
    
    __tablename__ = "landmarks"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text)
    short_description = Column(String(500))
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    city = Column(String(100), nullable=False)
    category = Column(String(100))
    rating = Column(Float, default=0.0)
    image_url = Column(String(500))
    audio_url = Column(String(500))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    def __repr__(self):
        return f"<Landmark(id={self.id}, name={self.name})>"