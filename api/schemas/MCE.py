from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class MCEBase(BaseModel):
    access_code: str
    creation_date: datetime
    update_date: Optional[datetime] = None
    agent_id: int
    elicitation_id: int

class MCECreate(MCEBase):
    pass

class MCE(MCEBase):
    id: int

    class Config:
        from_attributes = True
