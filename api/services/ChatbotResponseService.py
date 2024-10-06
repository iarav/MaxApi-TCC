from typing import Dict, Any
from fastapi import HTTPException
from sqlalchemy.orm import Session
from ..repository.MCERepository import MCERepository
from ..repository.ChatHistoryRepository import ChatHistoryRepository
from ..repository.ConceptRepository import ConceptRepository
from ..repository.ConceptRelationRepository import ConceptRelationRepository
from ..schemas import Chat as SchemaChat
from ..schemas import MCE as SchemaMCE
from ..schemas import Concept as SchemaConcept
from ..schemas import ConceptRelation as SchemaConceptRelation
from ..schemas import Elicitation as SchemaElicitation
from ..crud import Elicitation as CrudElicitation
from ..crud import ChatHistory as CrudChatHistory
from ..crud import Concept as CrudConcept
from ..crud import ConceptRelation as CrudConceptRelation
from ..chatbot.MaxBot import MaxBot
from ..chatbot.MaxElicitationSteps import Steps, getPreviousStep
from ..chatbot.BeliefMatrix import getBeliefByAnswer
from ..helper.ErrorHandler import handleException, handleError
from ..chatbot.ResponseProcessor import ResponseProcessor, AlternativeResponses, YesMaybeOrNotResponses
from ..chatbot.MaxBotProperties import MaxBotProperties

def generateChatbotResponseByUserInput(userData: SchemaChat.CreateUserInput, db: Session) -> Dict[str, Any]:
    try:
        mce = MCERepository.getMCE(userData.access_code, db=db)
        chatbotResponse, step = _generateChatResponse(db, userData, mce)
        userInput = userData.user_input
        
        if step is None:
            raise HTTPException(status_code=400, detail=chatbotResponse)

        _registerChatHistory(userInput, chatbotResponse, step, db=db, mceId=mce.id)

        return {"message": "Success", "response": chatbotResponse}

    except Exception as e:
        handleException(e)

def _registerChatHistory(userInput: str, chatbotResponse: str, step: str, db: Session, mceId: int) -> None:
    previousStep = None
    if step == Steps.STEP_UNKNOWN.value or step == Steps.STEP_UNKNOWN:
        previousStep = Steps.STEP_UNKNOWN.value
    else:
        if step == Steps.STEP_ONE.value or step == Steps.STEP_ONE:
            previousStep = None
        else:
            previousStep = ChatHistoryRepository.getLastStepByCurrentStep(db, mceId, step) 
            handleError(previousStep)
    
    if userInput:
        ChatHistoryRepository.addMessageToHistory(db, userInput, "agent", previousStep, mceId)
    if chatbotResponse:
        ChatHistoryRepository.addMessageToHistory(db, chatbotResponse, "chatbot", step, mceId)

def _generateChatResponse(db: Session, userData: SchemaChat.CreateUserInput, mce: SchemaMCE.MCE) -> tuple:
    chatbot = MaxBot()
    message = userData.user_input.strip().lower()
    secondConcept = None

    lastStepMessages = CrudChatHistory.getLastStepMessagesByMCE(db, mce.id)
    handleError(lastStepMessages)

    elicitation = CrudElicitation.getElicitationById(db, mce.elicitation_id)
    handleError(elicitation)
    
    currentConcept = CrudConcept.getMostRecentConceptByMCE(db, mce.id)
    handleError(currentConcept)

    processedMessage, secondConcept, processedStepTwoMessage, currentConceptRelationWithConcepts = _handleSteps(db, message, lastStepMessages, elicitation, mce, currentConcept)

    if isinstance(processedMessage, dict) and processedMessage.get("error"):
        return processedMessage.get("error"), Steps.STEP_UNKNOWN

    maxBotProperties = MaxBotProperties(message=processedMessage, mce=mce, elicitation=elicitation, currentConcept=currentConcept, lastStepMessages=lastStepMessages, stepTwoUserResponse=processedStepTwoMessage, secondConcept=secondConcept, currentConceptRelationWithConcepts=currentConceptRelationWithConcepts)
    
    return chatbot.sendMessage(properties=maxBotProperties)

def _handleSteps(db: Session, message: str, lastStepMessages: list, elicitation: SchemaElicitation.Elicitation, mce: SchemaMCE.MCE, currentConcept: SchemaConcept.Concept) -> tuple:
    processedMessage = message
    secondConcept = None
    processedStepTwoMessage = None
    currentConceptRelationWithConcepts = None
    error = False
    if lastStepMessages and len(lastStepMessages):
        lastStep = lastStepMessages[-1].step
        if lastStep == Steps.STEP_TWO.value:
            processedMessage = ResponseProcessor().processAlternativeQuestion(processedMessage)

        if lastStep == Steps.STEP_THREE_P1.value or lastStep == Steps.STEP_THREE_P2.value:
            stepTwoUserResponse = CrudChatHistory.getMessagesByStepAndSender(db, mce.id, Steps.STEP_TWO.value, "agent")
            stepTwoUserResponse = stepTwoUserResponse[-1].message if stepTwoUserResponse else None
            processedStepTwoMessage = ResponseProcessor().processAlternativeQuestion(stepTwoUserResponse)
            firstQuestionAsked = lastStep == Steps.STEP_THREE_P2.value
            concept = currentConcept.name if currentConcept else elicitation.concept
            processedMessage = _processStepThreeResponse(processedMessage, processedStepTwoMessage, concept, mce.id, firstQuestionAsked, db)
            
        if lastStep == Steps.STEP_CONDITION_ONE.value:
            processedMessage = ResponseProcessor().processAlternativeQuestion(processedMessage)
            
        if lastStep == Steps.STEP_THREE_P2.value or lastStep == Steps.STEP_FOUR.value:
            secondConceptData = None
            secondConceptRelation = None
            if lastStep == Steps.STEP_THREE_P2.value:
                secondConceptData = CrudConcept.getSecondConceptByMCE(db, mce.id)
                handleError(secondConceptData)
                if secondConceptData:
                    secondConceptRelation = CrudConceptRelation.getConceptRelationByConceptIds(db=db, concept2_id=secondConceptData.id)
                    handleError(secondConceptRelation)
            elif lastStep == Steps.STEP_FOUR.value:
                secondConceptData = _createConcept(db, processedMessage, mce.id)
                if isinstance(secondConceptData, dict) and secondConceptData.get("error"):
                    processedMessage = secondConceptData
                    error = True
                if (not error) and secondConceptData:
                    secondConceptRelation = _createConceptRelation(db, currentConcept, secondConceptData)
                
            if not error:    
                if secondConceptRelation:
                    secondConcept = SchemaConcept.ConceptWithRelation(
                        id=secondConceptData.id,
                        name=secondConceptData.name,
                        behavioral_belief=secondConceptData.behavioral_belief,
                        normative_belief=secondConceptData.normative_belief,
                        mce_id=secondConceptData.mce_id,
                        relation_verb=secondConceptRelation.relation_verb,
                        relation_weight=secondConceptRelation.relation_weight,
                        concept1_id=secondConceptRelation.concept1_id,
                        concept2_id=secondConceptRelation.concept2_id
                    )
                
                currentConceptRelationWithConcepts = ConceptRelationRepository.getCurrentConceptRelationAndConceptsByMCE(db, mce.id)
        
        if lastStep == Steps.STEP_FIVE.value:
            relationWeight = None
            currentConceptRelationWithConcepts = ConceptRelationRepository.getCurrentConceptRelationAndConceptsByMCE(db, mce.id)
            if not currentConceptRelationWithConcepts:
                raise HTTPException(status_code=500, detail="Error finding concept relation")
            processedMessage = ResponseProcessor().processYesOrNotQuestion(processedMessage)
            if isinstance(processedMessage, dict) and processedMessage.get("error"):
                error = True
            if not error:
                if processedMessage == YesMaybeOrNotResponses.YES.value:
                    relationWeight = "+"
                elif processedMessage == YesMaybeOrNotResponses.NOT.value:
                    relationWeight = "-"
                if relationWeight:
                    conceptRelation = SchemaConceptRelation.ConceptRelationCreate(
                        concept1_id=currentConceptRelationWithConcepts.concept1_id,
                        concept2_id=currentConceptRelationWithConcepts.concept2_id,
                        relation_weight=relationWeight
                    )
                    ConceptRelationRepository.addRelationWeightToConceptRelation(db, conceptRelation)
            
    return processedMessage, secondConcept, processedStepTwoMessage, currentConceptRelationWithConcepts

def _processStepThreeResponse(message: str, initialPositioning: str, concept: str, mceId: int, firstQuestionAsked: bool, db: Session) -> None:
    processedMessage = ResponseProcessor().processYesMaybeOrNotQuestion(message)
    if isinstance(processedMessage, dict) and processedMessage.get("error"):
        return processedMessage
    conceptObj = CrudConcept.getConceptByMCEAndName(db, mceId=mceId, name=concept)
    if not conceptObj:
        handleException("Concept not found")

    belief = getBeliefByAnswer(processedMessage)
    if (initialPositioning == AlternativeResponses.A.value and not firstQuestionAsked) or (initialPositioning == AlternativeResponses.B.value and firstQuestionAsked):
        conceptObj.behavioral_belief = belief
    else:
        conceptObj.normative_belief = belief

    CrudConcept.editConcept(db, concept=conceptObj)
    return processedMessage

def _createConcept(db: Session, concept: str, mceId: int) -> None:
    conceptObj = SchemaConcept.ConceptCreate(
        name=concept,
        mce_id=mceId
    )
    conceptObj = ConceptRepository.createIfNotExists(db, conceptObj)
    if conceptObj is None:
        return {"error" : "Por favor, forneça um conceito diferente."}
    return conceptObj

def _createConceptRelation(db: Session, firstConcept, secondConcept) -> SchemaConceptRelation.ConceptRelation:
    conceptRelation = SchemaConceptRelation.ConceptRelationCreate(
        relation_verb=None,
        relation_weight=None,
        concept1_id=firstConcept.id,
        concept2_id=secondConcept.id
    )
    conceptRelation = ConceptRelationRepository.createIfNotExists(db, conceptRelation)
    return conceptRelation
        
        