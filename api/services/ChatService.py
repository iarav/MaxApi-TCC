from fastapi import HTTPException
from sqlalchemy.orm import Session
from ..crud import Agent as crudAgent
from ..crud import Elicitation as crudElicitation
from ..crud import MCE as crudBase
from ..crud import Concept as crudConcept
from ..crud import ChatHistory as crudChatHistory
from ..schemas import Concept as schemaConcept
from ..schemas import ChatHistory as schemaChatHistory
from ..schemas import Agent as schemaAgent
from ..schemas import Elicitation as schemaElicitation
from ..schemas import MCE as schemaMCE
from ..schemas import Chat as schemaChat
from ..chatbot.MaxBot import MaxBot
from datetime import datetime
import random
import string
from typing import List, Dict, Any
from ..chatbot.MaxElicitationSteps import Steps, getPreviousStep
from ..chatbot.BeliefMatrix import BeliefMatrix, getBeliefByAnswer

def createChatbot(
    focalQuestion: schemaElicitation.ElicitationCreate,
    agent: schemaAgent.AgentCreate,
    db: Session
) -> schemaMCE.MCE:
    try:
        dbAgent = _createAgentIfNotExists(db, agent)
        dbElicitation = _createElicitationIfNotExists(db, focalQuestion)
        accessCode = _generateAccessCode(db)
        _createConcept(db, schemaConcept.ConceptCreate(name=focalQuestion.concept, mce_id=mce.id))
        mce = _createMCE(db, accessCode, dbAgent.id, dbElicitation.id)
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
        response, precessedUserInput = _generateChatResponse(db, user_data, mce)
        chatbot_response, step = response
        if step is None:
            raise HTTPException(status_code=400, detail=chatbot_response)
        _registerChatHistory(precessedUserInput, chatbot_response, step, db=db, mceId=mce.id)
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

def _generateChatResponse(db: Session, user_data: schemaChat.CreateUserInput, mce: schemaMCE.MCE) -> str:
    chatbot = MaxBot()
    message = user_data.user_input
    lastStepMessages = crudChatHistory.getLastStepMessagesByMCE(db, mce.id)
    _handleError(lastStepMessages)
    elicitation = crudElicitation.getElicitationById(db, mce.elicitation_id)
    _handleError(elicitation)
    if len(lastStepMessages) > 0 and lastStepMessages[-1].step == Steps.STEP_TWO.value:
        message = _processResponse(message)
    stepTwoUserResponse = None
    if lastStepMessages[-1].step == Steps.STEP_THREE_P1.value:
        stepTwoUserResponse = crudChatHistory.getMessagesByStepAndSender(db, mce.id, Steps.STEP_TWO.value, "agent")
        _processStepThreeResponse(message, stepTwoUserResponse[-1].message, elicitation.concept, mce.id, False, db)
    if lastStepMessages[-1].step == Steps.STEP_THREE_P2.value:
        stepTwoUserResponse = crudChatHistory.getMessagesByStepAndSender(db, mce.id, Steps.STEP_TWO.value, "agent")
        _processStepThreeResponse(message, stepTwoUserResponse[-1].message, elicitation.concept, mce.id, True, db)
    return chatbot.sendMessage(message, mce, elicitation, lastStepMessages, stepTwoUserResponse[-1].message), message

def _processResponse(message):
    responsesA = ['a', 'a.', 'a:', 'alternativa a', 'letra a']
    responsesB = ['b', 'b.', 'b:', 'alternativa b', 'letra b']
    
    response = message.strip().lower()
    
    if response in responsesA:
        return "A"
    elif response in responsesB:
        return "B"
    else:
        raise HTTPException(status_code=400, detail="Invalid response. Please, answer with A or B")


def _registerChatHistory(userInput: str, chatbot_response: str, step: str, db: Session, mceId: int) -> None:
    if userInput:
        previousStep = getPreviousStep(step)
        _addMessageToHistory(userInput, "agent", previousStep, db, mceId)
    if chatbot_response:
        _addMessageToHistory(chatbot_response, "chatbot", step, db, mceId)

def _addMessageToHistory(message: str, sender: str, step: str, db: Session, mceId: int) -> None:
    chatHistoryCreate = schemaChatHistory.ChatHistoryCreate(
        message=message,
        sender=sender,
        step=step,
        mce_id=mceId
    )
    response = crudChatHistory.addMessageToHistory(db, chatHistory=chatHistoryCreate)
    _handleError(response)

def _createAgentIfNotExists(db: Session, agent: schemaAgent.AgentCreate) -> schemaAgent.Agent:
    dbAgent = crudAgent.getAgentByEmail(db, email=agent.email)
    _handleError(dbAgent)
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
    _handleError(dbElicitation)
    return dbElicitation

def _generateAccessCode(db: Session) -> str:
    accessCode = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    while crudBase.getMCEByAccessCode(db, access_code=accessCode):
        accessCode = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    _handleError(accessCode)
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

def _createConcept(db: Session, concept: schemaConcept.ConceptCreate) -> schemaConcept.Concept:
    dbConcept = crudConcept.getConceptByMCEAndName(db, mce_id=concept.mce_id, name=concept.name)
    if not dbConcept:
        dbConcept = crudConcept.createConcept(db, concept=concept)
        _handleError(dbConcept)
    return dbConcept

def _processStepThreeResponse(message: str, initialPosicioning: str, concept: str, mce_id: int, firstQuestionAsked: bool,db: Session) -> str:
    possibleResponses = ["sim", "talvez", "não", "nao", "n", "s"]
    if message.lower() in possibleResponses:
        concept = crudConcept.getConceptByMCEAndName(db, mce_id=mce_id, name=concept)
        if not concept:
            raise HTTPException(status_code=404, detail="Concept not found")
        if (initialPosicioning == "A" and firstQuestionAsked == False) or (initialPosicioning == "B" and firstQuestionAsked == True):
            concept.behavioral_belief = getBeliefByAnswer(message)
        elif initialPosicioning == "B":
            concept.normative_belief = getBeliefByAnswer(message)
        crudConcept.editConcept(db, concept=concept)
    else:
        raise HTTPException(status_code=400, detail="Invalid response. Please, answer with 'sim', 'talvez' or 'não'")

def _handleError(response: Any) -> None:
    if isinstance(response, dict) and response.get("error"):
        raise HTTPException(status_code=500, detail=response.get("error"))

def _handleException(e: Exception) -> None:
    print(e)
    if isinstance(e, HTTPException):
        raise e
    raise HTTPException(status_code=500, detail=str(e))
