from pydantic import BaseModel
from typing import Optional

class ConceptRelationBase(BaseModel):
    concept1_id: int
    concept2_id: int
    relation_verb: Optional[str] = None
    relation_weight: Optional[str] = None

class ConceptRelationCreate(ConceptRelationBase):
    pass

class ConceptRelation(ConceptRelationBase):
    class Config:
        from_attributes = True
