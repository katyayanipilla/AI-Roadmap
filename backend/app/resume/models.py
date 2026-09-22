from sqlalchemy import Column, Integer, ForeignKey, Text, DateTime
from datetime import datetime
from app.database import Base

class Resume(Base):
    __tablename__ = "resumes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    content = Column(Text)
    score = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)