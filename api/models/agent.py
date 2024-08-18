from sqlalchemy import Column, Integer, String
from ..db import Base

class Agent(Base):
    __tablename__ = "agent"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
