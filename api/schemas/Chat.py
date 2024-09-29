from pydantic import BaseModel
from typing import Optional

class ChatBase(BaseModel):
    access_code: str
    user_input: str = ""

class CreateUserInput(ChatBase):
    pass
