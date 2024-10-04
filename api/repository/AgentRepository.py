from sqlalchemy.orm import Session
from ..crud import Agent as crudAgent
from ..schemas import Agent as schemaAgent

class AgentRepository:
    @staticmethod
    def createIfNotExists(db: Session, agent: schemaAgent.AgentCreate) -> schemaAgent.Agent:
        dbAgent = crudAgent.getAgentByEmail(db, email=agent.email)
        if not dbAgent:
            dbAgent = crudAgent.createAgent(db, agent=agent)
        return dbAgent