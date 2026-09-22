from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.database import Base
from sqlalchemy import Date


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    profile_image = Column(String, nullable=True)
    streak = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_quiz_date = Column(Date, nullable=True)