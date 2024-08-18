from sqlalchemy import Column, Integer, String, Text
from ..db import Base

class Elicitation(Base):
    __tablename__ = "elicitation"
    id = Column(Integer, primary_key=True, index=True)
    focal_question = Column(Text, nullable=False)
    agent = Column(String, nullable=True)
    concept = Column(String, nullable=True)
    domain = Column(String, nullable=True)
