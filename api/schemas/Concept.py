from pydantic import BaseModel

class ConceptBase(BaseModel):
    name: str
    behavioral_belief: str = None
    normative_belief: str = None
    mce_id: int

class ConceptCreate(ConceptBase):
    pass

class Concept(ConceptBase):
    id: int

    class Config:
        from_attributes = True
