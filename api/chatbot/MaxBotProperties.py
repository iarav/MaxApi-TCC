
class MaxBotProperties:
    def __init__(self, message = "", mce = None, elicitation = None, currentConcept = None, lastStepMessages = [], stepTwoUserResponse = None, secondConcept = None, currentConceptRelationWithConcepts = None):
        self.message = message
        self.mce = mce
        self.elicitation = elicitation
        self.currentConcept = currentConcept
        self.lastStepMessages = lastStepMessages
        self.stepTwoUserResponse = stepTwoUserResponse
        self.secondConcept = secondConcept
        self.currentConceptRelationWithConcepts = currentConceptRelationWithConcepts
    
    def getProperties(self):
        return self.message, self.mce, self.elicitation, self.currentConcept, self.lastStepMessages, self.stepTwoUserResponse, self.secondConcept, self.currentConceptRelationWithConcepts
