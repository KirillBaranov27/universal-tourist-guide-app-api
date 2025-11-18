from sqlalchemy import Column, Integer, String, Text
from app.core.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)  # Убедись, что это String, а не Text
    full_name = Column(String(255), nullable=False)