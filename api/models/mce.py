from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from ..db import Base

class MCE(Base):
    __tablename__ = "mce"
    id = Column(Integer, primary_key=True, index=True)
    creation_date = Column(DateTime, nullable=False)
    access_code = Column(String, nullable=False)
    update_date = Column(DateTime)
    agent_id = Column(Integer, ForeignKey("agent.id"))
    elicitation_id = Column(Integer, ForeignKey("elicitation.id"))

    agent = relationship("Agent")
    elicitation = relationship("Elicitation")
