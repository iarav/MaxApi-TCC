from sqlalchemy import Column, Integer, String, Text, ForeignKey
from ..db import Base

class Concept(Base):
    __tablename__ = "concept"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    behavioral_belief = Column(Text, nullable=True)
    normative_belief = Column(Text, nullable=True)
    mce_id = Column(Integer, ForeignKey("mce.id"))
