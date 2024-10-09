from pydantic import BaseModel
from typing import Optional

class ConceptRelationBase(BaseModel):
    concept1_id: int
    concept2_id: int
    relation_weight: Optional[str] = None

class ConceptRelationCreate(ConceptRelationBase):
    pass

class ConceptRelation(ConceptRelationBase):
    class Config:
        from_attributes = True
        
class ConceptRelationWithConcepts(ConceptRelationBase):
    concept1_name: Optional[str] = None
    concept2_name: Optional[str] = None
    concept1_behavioral_belief: Optional[str] = None
    concept1_normative_belief: Optional[str] = None
    concept2_behavioral_belief: Optional[str] = None
    concept2_normative_belief: Optional[str] = None
    mce_id: Optional[int] = None
