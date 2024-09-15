from sqlalchemy.orm import Session
from ..models.Agent import Agent
from ..schemas.Agent import AgentCreate

def getAgents(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Agent).offset(skip).limit(limit).all()

def getAgentByEmail(db: Session, email: str):
    return db.query(Agent).filter(Agent.email == email).first()

def createAgent(db: Session, agent: AgentCreate):
    db_agent = Agent(email=agent.email, name=agent.name)
    db.add(db_agent)
    db.commit()
    db.refresh(db_agent)
    return db_agent
