from typing import Dict, Any
from fastapi import HTTPException
from sqlalchemy.orm import Session
from ..repository.MCERepository import MCERepository
from ..repository.ChatHistoryRepository import ChatHistoryRepository
from ..schemas import Chat as SchemaChat
from ..schemas import MCE as SchemaMCE
from ..crud import Elicitation as CrudElicitation
from ..crud import ChatHistory as CrudChatHistory
from ..crud import Concept as CrudConcept
from ..chatbot.MaxBot import MaxBot
from ..chatbot.MaxElicitationSteps import Steps, getPreviousStep
from ..chatbot.BeliefMatrix import getBeliefByAnswer
from ..helper.ErrorHandler import handleException, handleError

def generateChatbotResponseByUserInput(userData: SchemaChat.CreateUserInput, db: Session) -> Dict[str, Any]:
    try:
        mce = MCERepository.getMCE(userData.access_code, db=db)
        response, processedInput = _generateChatResponse(db, userData, mce)
        chatbotResponse, step = response

        if step is None:
            raise HTTPException(status_code=400, detail=chatbotResponse)

        if step is not Steps.STEP_UNKNOWN:
            _registerChatHistory(processedInput, chatbotResponse, step, db=db, mceId=mce.id)

        return {"message": "Success", "response": chatbotResponse}

    except Exception as e:
        handleException(e)

def _generateChatResponse(db: Session, userData: SchemaChat.CreateUserInput, mce: SchemaMCE.MCE) -> tuple:
    chatbot = MaxBot()
    message = userData.user_input.strip().lower()
    
    lastStepMessages = CrudChatHistory.getLastStepMessagesByMCE(db, mce.id)
    handleError(lastStepMessages)

    elicitation = CrudElicitation.getElicitationById(db, mce.elicitation_id)
    handleError(elicitation)

    if lastStepMessages and lastStepMessages[-1].step == Steps.STEP_TWO.value:
        message = _processResponse(message)

    stepTwoUserResponse = None
    if lastStepMessages:
        if lastStepMessages[-1].step == Steps.STEP_THREE_P1.value:
            stepTwoUserResponse = CrudChatHistory.getMessagesByStepAndSender(db, mce.id, Steps.STEP_TWO.value, "agent")
            _processStepThreeResponse(message, stepTwoUserResponse[-1].message, elicitation.concept, mce.id, False, db)
        elif lastStepMessages[-1].step == Steps.STEP_THREE_P2.value:
            stepTwoUserResponse = CrudChatHistory.getMessagesByStepAndSender(db, mce.id, Steps.STEP_TWO.value, "agent")
            _processStepThreeResponse(message, stepTwoUserResponse[-1].message, elicitation.concept, mce.id, True, db)

    stepTwoUserResponseMessage = stepTwoUserResponse[-1].message if stepTwoUserResponse else None
    return chatbot.sendMessage(message, mce, elicitation, lastStepMessages, stepTwoUserResponseMessage), message

def _processResponse(message: str) -> str:
    validResponses = {
        "a": "A", "a.": "A", "a:": "A", "alternativa a": "A", "letra a": "A",
        "b": "B", "b.": "B", "b:": "B", "alternativa b": "B", "letra b": "B"
    }

    response = message.strip().lower()
    if response in validResponses:
        return validResponses[response]
    else:
        # TODO - Add a way to handle this error as answer not exception
        raise HTTPException(status_code=400, detail="Invalid response. Please, answer with A or B")

def _registerChatHistory(userInput: str, chatbotResponse: str, step: str, db: Session, mceId: int) -> None:
    previousStep = getPreviousStep(step)
    
    if userInput:
        ChatHistoryRepository.addMessageToHistory(db, userInput, "agent", previousStep, mceId)
    if chatbotResponse:
        ChatHistoryRepository.addMessageToHistory(db, chatbotResponse, "chatbot", step, mceId)

def _processStepThreeResponse(message: str, initialPositioning: str, concept: str, mceId: int, firstQuestionAsked: bool, db: Session) -> None:
    validResponses = {"sim", "talvez", "não", "nao", "n", "s"}
    
    if message.lower() in validResponses:
        conceptObj = CrudConcept.getConceptByMCEAndName(db, mceId=mceId, name=concept)
        if not conceptObj:
            raise HTTPException(status_code=404, detail="Concept not found")

        if (initialPositioning == "A" and not firstQuestionAsked) or (initialPositioning == "B" and firstQuestionAsked):
            conceptObj.behavioralBelief = getBeliefByAnswer(message)
        elif initialPositioning == "B":
            conceptObj.normativeBelief = getBeliefByAnswer(message)

        # TODO - make this edit work correctly
        CrudConcept.editConcept(db, concept=conceptObj)
    else:
        # TODO - Add a way to handle this error as answer not exception
        raise HTTPException(status_code=400, detail="Invalid response. Please, answer with 'sim', 'talvez' or 'não'")
