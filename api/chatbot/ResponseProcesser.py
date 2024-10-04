from fastapi import HTTPException
from enum import Enum

class YesMaybeOrNotResponses(Enum):
    YES = "sim"
    MAYBE = "talvez"
    NOT = "não"

class AlternativeResponses(Enum):
    A = "A"
    B = "B"

class ResponseProcesser():
    def __init__(self):
        self.response = None

    def processYesMaybeOrNotQuestion(self, message: str) -> str:
        validYesResponses = {"sim", "s"}
        validMaybeResponses = {"talvez"}
        validNotResponses = {"não", "nao", "n"}
        validResponses = validYesResponses.union(validMaybeResponses).union(validNotResponses)

        response = message.strip().lower()
        if response in validResponses:
            if response in validYesResponses:
                self.response = YesMaybeOrNotResponses.YES.value
            elif response in validMaybeResponses:
                self.response = YesMaybeOrNotResponses.MAYBE.value
            elif response in validNotResponses:
                self.response = YesMaybeOrNotResponses.NOT.value
            return self.response
        else:
            # TODO - Add a way to handle this error as answer not exception
            raise HTTPException(status_code=400, detail="Invalid response. Please, answer with Yes, Maybe or Not")
    
    def processAlternativeQuestion(self, message: str) -> str:
        validAResponses = {"a", "a.", "a:", "alternativa a", "letra a"}
        validBResponses = {"b", "b.", "b:", "alternativa b", "letra b"}
        validResponses = validAResponses.union(validBResponses)

        response = message.strip().lower()
        if response in validResponses:
            if response in validAResponses:
                self.response = AlternativeResponses.A.value
            elif response in validBResponses:
                self.response = AlternativeResponses.B.value
            return self.response
        else:
            # TODO - Add a way to handle this error as answer not exception
            print("Invalid response. Please, answer with A or B, message: " + message)
            raise HTTPException(status_code=400, detail="Invalid response. Please, answer with A or B")