from pydantic import BaseModel

class AgentBase(BaseModel):
    email: str
    name: str

class AgentCreate(AgentBase):
    pass

class Agent(AgentBase):
    id: int

    class Config:
        from_attributes = True
