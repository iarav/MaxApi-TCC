from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship
from ..db import Base
from datetime import datetime

class ChatHistory(Base):
    __tablename__ = "chat_history"

    id = Column(Integer, primary_key=True, index=True)
    message = Column(Text, nullable=False)
    sender = Column(String(10), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    mce_id = Column(Integer, ForeignKey("mce.id"))

    mce = relationship("MCE")

    __table_args__ = (
        CheckConstraint(sender.in_(['chatbot', 'agent']), name="check_sender"),
    )
