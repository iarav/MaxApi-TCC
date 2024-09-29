from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from ..models.Agent import Agent
from ..schemas.Agent import AgentCreate

def getAgents(db: Session, skip: int = 0, limit: int = 10):
    try:
        return db.query(Agent).offset(skip).limit(limit).all()
    except SQLAlchemyError as e:
        return {"error": str(e)}

def getAgentByEmail(db: Session, email: str):
    try:
        return db.query(Agent).filter(Agent.email == email).first()
    except SQLAlchemyError as e:
        return {"error": str(e)}

def createAgent(db: Session, agent: AgentCreate):
    try:
        dbAgent = Agent(email=agent.email, name=agent.name)
        db.add(dbAgent)
        db.commit()
        db.refresh(dbAgent)
        return dbAgent
    except SQLAlchemyError as e:
        db.rollback()
        return {"error": str(e)}
