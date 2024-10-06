from sqlalchemy import Column, Integer, ForeignKey, String, CHAR
from ..db import Base

class ConceptRelation(Base):
    __tablename__ = "concept_relation"
    concept1_id = Column(Integer, ForeignKey("concept.id"), primary_key=True)
    concept2_id = Column(Integer, ForeignKey("concept.id"), primary_key=True)
    relation_verb = Column(String, nullable=True)
    relation_weight = Column(CHAR, nullable=True)
