from sqlalchemy import Column, String, Text, DateTime
from sqlalchemy.sql import func
from .database import Base

class ChatMemory(Base):
    __tablename__ = "chat_memory"

    id = Column(String, primary_key=True)
    session_id = Column(String, index=True)
    role = Column(String)
    message = Column(Text)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
