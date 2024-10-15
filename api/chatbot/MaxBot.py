
from .MaxResponses import MaxResponses
from .MaxElicitationSteps import Steps, getNextStep
from .ResponseProcessor import AlternativeResponses
from .MaxBotProperties import MaxBotProperties
from fastapi import HTTPException
class MaxBot:
    def __init__(self):
        self.name = "MAX"
        self.nameMeaning = "Management and Acquisition eXpert"

    def getName(self):
        return self.name
    
    def getNameMeaning(self):
        return self.nameMeaning
    
    def sendMessage(self, properties: MaxBotProperties):
        message, mce, elicitation, currentConcept, lastStepMessages, stepTwoUserResponse, secondConcept, currentConceptRelationWithConcepts = properties.getProperties()
        if message == "" and len(lastStepMessages) == 0:
            return self._stepOne(mce, elicitation), Steps.STEP_ONE
        else:
            if message == "":
                return MaxResponses.unknown(), Steps.STEP_UNKNOWN
            if len(lastStepMessages) > 0:
                lastStep = lastStepMessages[-1].step
                nextStep = getNextStep(lastStep)
                concept = currentConcept.name if currentConcept else elicitation.concept
                # Belief Matrix Positioning
                if nextStep == Steps.STEP_TWO.value:
                    if lastStep == Steps.STEP_FOUR.value or lastStep == Steps.STEP_EIGHT.value:
                        concept = message
                    return self._stepTwo(elicitation, concept), nextStep
                elif nextStep == Steps.STEP_THREE_P1.value:
                    return self._stepThree(elicitation, message, False, concept), nextStep
                elif nextStep == Steps.STEP_THREE_P2.value:
                    return self._stepThree(elicitation, stepTwoUserResponse, True, concept), nextStep
                elif nextStep == Steps.STEP_CONDITION_ONE.value:
                    if secondConcept is None:
                        return self._stepFour(concept), Steps.STEP_FOUR.value
                    else:
                        if secondConcept.relation_weight is None:   
                            return self._stepFive(currentConceptRelationWithConcepts), Steps.STEP_FIVE.value
                        else:
                            return self._stepSix(concept), Steps.STEP_SIX.value
                elif nextStep == Steps.STEP_FIVE.value:
                    return self._stepFive(currentConceptRelationWithConcepts), nextStep
                elif nextStep == Steps.STEP_FIVE_P1.value:
                    return self._stepFiveP1(elicitation.focal_question, currentConceptRelationWithConcepts), nextStep
                elif nextStep == Steps.STEP_CONDITION_TWO.value:
                    if message == AlternativeResponses.A.value:
                        return self._stepEight(), Steps.STEP_EIGHT.value
                    elif message == AlternativeResponses.B.value:
                        return self._stepNine(), Steps.STEP_NINE.value
                    elif message == AlternativeResponses.C.value:
                        return self._stepEnd(), Steps.STEP_END.value
                elif nextStep == Steps.STEP_SEVEN.value:
                    return self._stepSeven(concept, message), nextStep
                elif nextStep == Steps.STEP_NINE_P2.value:
                    return self._stepNinePartTwo(message), Steps.STEP_NINE_P2.value
                else:
                    return MaxResponses.unknown(), Steps.STEP_UNKNOWN
            else:
                return "To begin the chat, send an empty string as user_input", None
            

    def _stepOne(self, mce, elicitation):
        response = MaxResponses.greeting(mce.agent.name.capitalize(), self.name, self.nameMeaning) + MaxResponses.explainingFocalQuestion(elicitation.focal_question)
        return response
    
    def _stepTwo(self, elicitation, concept):
        response = MaxResponses.goingDeeper(concept) + MaxResponses.makingInitialPositioning(elicitation.agent, concept, elicitation.domain)
        return response
    
    def _stepThree(self, elicitation, initialPositioning, firstQuestionAsked, concept):
        response = ""
        if (initialPositioning == AlternativeResponses.A.value and firstQuestionAsked == False) or (initialPositioning == AlternativeResponses.B.value and firstQuestionAsked == True):
            response = MaxResponses.determineBehavioralBelieve(elicitation.agent.capitalize(), concept, elicitation.domain)
        else:
            response = MaxResponses.normativeBelieve(concept.capitalize(), elicitation.domain)
        return response
    
    def _stepFour(self, concept):
        response = MaxResponses.secondConcept(concept)
        return response
    
    def _stepFive(self, currentConceptRelationWithConcepts):
        concept1 = None
        concept2 = None    
        if currentConceptRelationWithConcepts:
            concept1 = currentConceptRelationWithConcepts.concept1_name
            concept2 = currentConceptRelationWithConcepts.concept2_name
        else:
            raise HTTPException(status_code=500, detail="Error finding concept relation")
        response = MaxResponses.defineRelationWeight(concept1, concept2)
        return response
    
    def _stepFiveP1(self, focalQuestion, currentConceptRelationWithConcepts):
        concept1 = None
        concept2 = None    
        relationWeight = None
        response = ""
        if currentConceptRelationWithConcepts:
            concept1 = currentConceptRelationWithConcepts.concept1_name
            concept2 = currentConceptRelationWithConcepts.concept2_name
            relationWeight = currentConceptRelationWithConcepts.relation_weight
        else:
            raise HTTPException(status_code=500, detail="Error finding concept relation")
        if relationWeight == "+":
            response = MaxResponses.concludeConceptsRelationPositiveWeight(focalQuestion, concept1, concept2)
        elif relationWeight == "-":
            response = MaxResponses.concludeConceptsRelationNegativeWeight(focalQuestion, concept1, concept2)
        response = response + MaxResponses.concludeConceptsRelationShowingOptions()
        return response
    
    def _stepSix(self, newConcept):
        return MaxResponses.addRelationOfNewConceptToAnotherConcept(newConcept)
    
    def _stepSeven(self, concept1, concept2):
        return MaxResponses.defineRelationDirection(concept1, concept2)
    
    def _stepEight(self):
        return MaxResponses.addNewConcept()
    
    def _stepNine(self):
        return MaxResponses.createRelationBetweenConceptsFirstConcept()
    
    def _stepNinePartTwo(self, firstConcept):
        return MaxResponses.createRelationBetweenConceptsSecondConcept(firstConcept)
    
    def _stepEnd(self):
        return MaxResponses.endArgumentation()
