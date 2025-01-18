from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from database.database import Base

class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index = True)
    title = Column(String, nullable=False)
    initial_timestamp = Column(DateTime, default=datetime.utcnow)
    last_update = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)