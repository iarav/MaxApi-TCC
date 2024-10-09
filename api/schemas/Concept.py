from pydantic import BaseModel
from typing import Optional

class ConceptBase(BaseModel):
    name: str
    behavioral_belief: Optional[str] = None
    normative_belief: Optional[str] = None
    mce_id: int

class ConceptCreate(ConceptBase):
    pass

class Concept(ConceptBase):
    id: int

    class Config:
        from_attributes = True

class ConceptWithRelation(ConceptBase):
    id: Optional[int] = None
    relation_weight: Optional[str] = None
    concept1_id: Optional[int] = None
    concept2_id: Optional[int] = None