from pydantic import BaseModel
from typing import Optional

class ElicitationBase(BaseModel):
    focal_question: str
    agent: Optional[str] = None
    concept: Optional[str] = None
    domain: Optional[str] = None

class ElicitationCreate(ElicitationBase):
    pass

class Elicitation(ElicitationBase):
    id: int

    class Config:
        orm_mode = True

class ElicitationStatus(ElicitationBase):
    id: Optional[int]
    isRegistered: bool = True

    class Config:
        orm_mode = True
