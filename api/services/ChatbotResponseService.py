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
from ..chatbot.ResponseProcesser import ResponseProcesser, AlternativeResponses

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
    processedStepTwoMessage = None
    processedMessage = message

    lastStepMessages = CrudChatHistory.getLastStepMessagesByMCE(db, mce.id)
    handleError(lastStepMessages)

    elicitation = CrudElicitation.getElicitationById(db, mce.elicitation_id)
    handleError(elicitation)

    if lastStepMessages and len(lastStepMessages):
        if lastStepMessages[-1].step == Steps.STEP_TWO.value:
            processedMessage = ResponseProcesser().processAlternativeQuestion(message)

        if lastStepMessages[-1].step == Steps.STEP_THREE_P1.value or lastStepMessages[-1].step == Steps.STEP_THREE_P2.value:
            stepTwoUserResponse = CrudChatHistory.getMessagesByStepAndSender(db, mce.id, Steps.STEP_TWO.value, "agent")
            stepTwoUserResponse = stepTwoUserResponse[-1].message if stepTwoUserResponse else None
            processedStepTwoMessage = ResponseProcesser().processAlternativeQuestion(stepTwoUserResponse)
            firstQuestionAsked = lastStepMessages[-1].step == Steps.STEP_THREE_P2.value
            processedMessage = _processStepThreeResponse(message, processedStepTwoMessage, elicitation.concept, mce.id, firstQuestionAsked, db)

    return chatbot.sendMessage(processedMessage, mce, elicitation, lastStepMessages, processedStepTwoMessage), message

def _registerChatHistory(userInput: str, chatbotResponse: str, step: str, db: Session, mceId: int) -> None:
    previousStep = getPreviousStep(step)
    
    if userInput:
        ChatHistoryRepository.addMessageToHistory(db, userInput, "agent", previousStep, mceId)
    if chatbotResponse:
        ChatHistoryRepository.addMessageToHistory(db, chatbotResponse, "chatbot", step, mceId)

def _processStepThreeResponse(message: str, initialPositioning: str, concept: str, mceId: int, firstQuestionAsked: bool, db: Session) -> None:
    processedMessage = ResponseProcesser().processYesMaybeOrNotQuestion(message)
    conceptObj = CrudConcept.getConceptByMCEAndName(db, mceId=mceId, name=concept)
    if not conceptObj:
        handleException("Concept not found")

    belief = getBeliefByAnswer(processedMessage)
    print("Belief: ", belief)
    if (initialPositioning == AlternativeResponses.A.value and not firstQuestionAsked) or (initialPositioning == AlternativeResponses.B.value and firstQuestionAsked):
        conceptObj.behavioral_belief = belief
    else:
        conceptObj.normative_belief = belief

    # TODO - make this edit work correctly
    CrudConcept.editConcept(db, concept=conceptObj)
    return processedMessage
