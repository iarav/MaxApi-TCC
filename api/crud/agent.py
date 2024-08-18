from sqlalchemy.orm import Session
from ..models.agent import Agent
from ..schemas.agent import AgentCreate

def get_agents(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Agent).offset(skip).limit(limit).all()

def get_agent_by_email(db: Session, email: str):
    return db.query(Agent).filter(Agent.email == email).first()

def create_agent(db: Session, agent: AgentCreate):
    db_agent = Agent(email=agent.email, name=agent.name)
    db.add(db_agent)
    db.commit()
    db.refresh(db_agent)
    return db_agent
