from fastapi import HTTPException
from sqlalchemy.orm import Session
from ..crud import Agent as crudAgent
from ..crud import Elicitation as crudElicitation
from ..crud import MCE as crudBase
from ..crud import ChatHistory as crudChatHistory
from ..schemas import ChatHistory as schemaChatHistory
from ..schemas import Agent as schemaAgent
from ..schemas import Elicitation as schemaElicitation
from ..schemas import MCE as schemaMCE
from ..schemas import Chat as schemaChat
from ..chatbot.MaxResponses import MaxResponses
from datetime import datetime
import random
import string
from typing import List, Dict, Any

def createChatbot(
    focalQuestion: schemaElicitation.ElicitationCreate,
    agent: schemaAgent.AgentCreate,
    db: Session
) -> schemaMCE.MCE:
    try:
        dbAgent = _createAgentIfNotExists(db, agent)
        _handleError(dbAgent)
        dbElicitation = _createElicitationIfNotExists(db, focalQuestion)
        _handleError(dbElicitation)
        accessCode = _generateAccessCode(db)
        _handleError(accessCode)
        mce = _createMCE(db, accessCode, dbAgent.id, dbElicitation.id)
        _handleError(mce)
        return mce
    except Exception as e:
        _handleException(e)

def signInAgent(access_code: str, db: Session) -> Dict[str, str]:
    try:
        mce = crudBase.getMCEByAccessCode(db, access_code=access_code)
        if not mce:
            raise HTTPException(status_code=401, detail="Unauthorized - invalid Access code")
        return {"message": "Success", "access_code": access_code}
    except Exception as e:
        _handleException(e)

def getAllChatHistory(access_code: str, db: Session) -> List[schemaChatHistory.ChatHistory]:
    try:
        mce = _getMCE(access_code, db=db)
        chatHistory = _getChatHistory(mce, db=db)
        return chatHistory
    except Exception as e:
        _handleException(e)

def generateChatbotResponseByUserInput(user_data: schemaChat.CreateUserInput, db: Session) -> Dict[str, Any]:
    try:
        mce = _getMCE(user_data.access_code, db=db)
        chatHistory = _getChatHistory(mce, db=db)
        chatbot_response = _generateChatResponse(user_data, mce, chatHistory)
        _registerChatHistory(user_data.user_input, chatbot_response, db=db, mceId=mce.id)
        return {"message": "Success", "response": chatbot_response}
    except Exception as e:
        _handleException(e)

def _getMCE(access_code: str, db: Session) -> schemaMCE.MCE:
    mce = crudBase.getMCEByAccessCode(db, access_code=access_code)
    if not mce:
        raise HTTPException(status_code=404, detail="Access code not found")
    return mce

def _getChatHistory(mce: schemaMCE.MCE, db: Session) -> List[schemaChatHistory.ChatHistory]:
    chatHistory = crudChatHistory.getMessageHistoryByMCE(db, mce_id=mce.id)
    _handleError(chatHistory)
    return chatHistory

def _generateChatResponse(user_data: schemaChat.CreateUserInput, mce: schemaMCE.MCE, chatHistory: List[schemaChatHistory.ChatHistory]) -> str:
    if user_data.user_input == "":
        return MaxResponses.greeting(mce.agent.name.capitalize())
    return f"Resposta do chatbot para o input: {user_data.user_input}"

def _registerChatHistory(userInput: str, chatbot_response: str, db: Session, mceId: int) -> None:
    if userInput:
        _addMessageToHistory(userInput, "agent", db, mceId)
    if chatbot_response:
        _addMessageToHistory(chatbot_response, "chatbot", db, mceId)

def _addMessageToHistory(message: str, sender: str, db: Session, mceId: int) -> None:
    chatHistoryCreate = schemaChatHistory.ChatHistoryCreate(
        message=message,
        sender=sender,
        mce_id=mceId
    )
    response = crudChatHistory.addMessageToHistory(db, chatHistory=chatHistoryCreate)
    _handleError(response)

def _createAgentIfNotExists(db: Session, agent: schemaAgent.AgentCreate) -> schemaAgent.Agent:
    dbAgent = crudAgent.getAgentByEmail(db, email=agent.email)
    if not dbAgent:
        dbAgent = crudAgent.createAgent(db, agent=agent)
        _handleError(dbAgent)
    return dbAgent

def _createElicitationIfNotExists(db: Session, focalQuestion: schemaElicitation.ElicitationCreate) -> schemaElicitation.Elicitation:
    dbElicitation = crudElicitation.getElicitationByFocalQuestion(db, focalQuestion=focalQuestion.focal_question)
    if not dbElicitation:
        dbElicitation = crudElicitation.createElicitation(db, elicitation=focalQuestion)
        if not dbElicitation:
            raise HTTPException(status_code=400, detail="The params agent, concept, and domain must be provided in the body, inside the focal question")
    return dbElicitation

def _generateAccessCode(db: Session) -> str:
    accessCode = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    while crudBase.getMCEByAccessCode(db, access_code=accessCode):
        accessCode = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    return accessCode

def _createMCE(db: Session, accessCode: str, agentId: int, elicitationId: int) -> schemaMCE.MCE:
    mce = schemaMCE.MCECreate(
        access_code=accessCode,
        creation_date=datetime.now(),
        update_date=datetime.now(),
        agent_id=agentId,
        elicitation_id=elicitationId
    )
    
    dbMCE = crudBase.createMCE(db, mce=mce)
    _handleError(dbMCE)
    return dbMCE

def _handleError(response: Any) -> None:
    if isinstance(response, dict) and response.get("error"):
        raise HTTPException(status_code=500, detail=response.get("error"))

def _handleException(e: Exception) -> None:
    print(e)
    if isinstance(e, HTTPException):
        raise e
    raise HTTPException(status_code=500, detail=str(e))
