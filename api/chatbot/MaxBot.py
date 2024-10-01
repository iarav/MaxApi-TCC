
from .MaxResponses import MaxResponses
from .MaxElicitationSteps import Steps, getNextStep
from ..crud.ChatHistory import getMessagesByStepAndSender

class MaxBot:
    def __init__(self):
        self.name = "MAX"
        self.nameMeaning = "Management and Acquisition eXpert"

    def getName(self):
        return self.name
    
    def getNameMeaning(self):
        return self.nameMeaning
    
    def sendMessage(self, message, mce = None, elicitation = None, lastStepMessages = None):
        if message == "" and len(lastStepMessages) == 0:
            return self._stepOne(mce, elicitation), Steps.STEP_ONE
        else:
            if message == "":
                return MaxResponses.unknown(), None
            if len(lastStepMessages) > 0:
                lastStep = lastStepMessages[-1].step
                nextStep = getNextStep(lastStep)
                if lastStep == Steps.STEP_ONE.value:
                    return self._stepTwo(elicitation), nextStep
                elif lastStep == Steps.STEP_TWO.value:
                    return self._stepThree(elicitation, message, False), nextStep
                elif lastStep == Steps.STEP_THREE_P1.value:
                    messages = getMessagesByStepAndSender(mce.id, Steps.STEP_TWO.value, "agent")
                    initialPosicioning = messages[-1].message
                    return self._stepThree(elicitation, initialPosicioning, True), nextStep
                else:
                    return MaxResponses.unknown(), None
            else:
                return "To beggin the chat, send an empty string as user_input", None
            

    def _stepOne(self, mce, elicitation):
        response = MaxResponses.greeting(mce.agent.name.capitalize(), self.name, self.nameMeaning) + MaxResponses.explainingFocalQuestion(elicitation.focal_question)
        return response
    
    def _stepTwo(self, elicitation):
        response = MaxResponses.goingDeeper() + MaxResponses.makingInitialPosicioning(elicitation.agent, elicitation.concept, elicitation.domain)
        print(response)
        return response
    
    def _stepThree(self, elicitation, initialPosicioning, firstQuestionAsked):
        response = ""
        if (initialPosicioning == "A" and firstQuestionAsked == False) or (initialPosicioning == "B" and firstQuestionAsked == True):
            response = MaxResponses.determineComportamentalBelieve(elicitation.agent.capitalize(), elicitation.concept, elicitation.domain)
        elif initialPosicioning == "B":
            response = MaxResponses.normativeBelieve(elicitation.concept.capitalize(), elicitation.domain)
        return response
