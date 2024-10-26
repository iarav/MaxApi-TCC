from sqlalchemy import Column, Integer, ForeignKey, DateTime, CHAR
from ..db import Base

class ConceptRelation(Base):
    __tablename__ = "concept_relation"
    concept1_id = Column(Integer, ForeignKey("concept.id"), primary_key=True)
    concept2_id = Column(Integer, ForeignKey("concept.id"), primary_key=True)
    relation_weight = Column(CHAR, nullable=True)
    creation_date = Column(DateTime, nullable=False)
