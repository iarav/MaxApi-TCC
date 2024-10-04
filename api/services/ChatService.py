from fastapi import HTTPException
from sqlalchemy.orm import Session
from ..crud import MCE as crudBase
from ..schemas import Concept as schemaConcept
from ..schemas import ChatHistory as schemaChatHistory
from ..schemas import Agent as schemaAgent
from ..schemas import Elicitation as schemaElicitation
from ..schemas import MCE as schemaMCE
from typing import List, Dict, Any
from ..helper.AccessCodeGenerator import AccessCodeGenerator
from ..repository.AgentRepository import AgentRepository
from ..repository.ElicitationRepository import ElicitationRepository
from ..repository.MCERepository import MCERepository
from ..repository.ChatHistoryRepository import ChatHistoryRepository
from ..repository.ConceptRepository import ConceptRepository
from ..helper.ErrorHandler import handleError, handleException

def createChatbot(
    focalQuestion: schemaElicitation.ElicitationCreate,
    agent: schemaAgent.AgentCreate,
    db: Session
) -> schemaMCE.MCE:
    try:
        dbAgent = AgentRepository.createIfNotExists(db, agent)
        handleError(dbAgent)
        dbElicitation = ElicitationRepository.createIfNotExists(db, focalQuestion)
        accessCode = AccessCodeGenerator.generateAccessCode(db)
        mce = MCERepository.createMCE(db, accessCode, dbAgent.id, dbElicitation.id)
        handleError(mce)
        ConceptRepository.createIfNotExists(db, schemaConcept.ConceptCreate(name=focalQuestion.concept, mce_id=mce.id))
        return mce
    except Exception as e:
        handleException(e)

def signInAgent(access_code: str, db: Session) -> Dict[str, str]:
    try:
        mce = crudBase.getMCEByAccessCode(db, access_code=access_code)
        if not mce:
            raise HTTPException(status_code=401, detail="Unauthorized - invalid Access code")
        return {"message": "Success", "access_code": access_code}
    except Exception as e:
        handleException(e)

def getAllChatHistory(access_code: str, db: Session) -> List[schemaChatHistory.ChatHistory]:
    try:
        mce = MCERepository.getMCE(access_code, db=db)
        chatHistory = ChatHistoryRepository.getChatHistory(mce, db=db)
        return chatHistory
    except Exception as e:
        handleException(e)
