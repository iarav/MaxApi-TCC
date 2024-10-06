from fastapi import HTTPException
from enum import Enum

class YesMaybeOrNotResponses(Enum):
    YES = "sim"
    MAYBE = "talvez"
    NOT = "não"

class AlternativeResponses(Enum):
    A = "A"
    B = "B"

class ResponseProcessor():
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
            return {"error": f"Por favor, responda com 'sim', 'talvez' ou 'não'. Sua resposta foi: {message}"}
        
    def processYesOrNotQuestion(self, message: str) -> str:
        validYesResponses = {"sim", "s"}
        validNotResponses = {"não", "nao", "n"}
        validResponses = validYesResponses.union(validNotResponses)

        response = message.strip().lower()
        if response in validResponses:
            if response in validYesResponses:
                self.response = YesMaybeOrNotResponses.YES.value
            elif response in validNotResponses:
                self.response = YesMaybeOrNotResponses.NOT.value
            return self.response
        else:
            return {"error": f"Por favor, responda com 'sim' ou 'não'. Sua resposta foi: {message}"}
    
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
            return {"error": f"Por favor, responda com 'A' ou 'B'. Sua resposta foi: {message}"}
    
    def processAlternativeABCQuestion(self, message: str) -> str:
        validAResponses = {"a", "a.", "a:", "alternativa a", "letra a"}
        validBResponses = {"b", "b.", "b:", "alternativa b", "letra b"}
        validCResponses = {"c", "c.", "c:", "alternativa c", "letra c"}
        validResponses = validAResponses.union(validBResponses).union(validCResponses)

        response = message.strip().lower()
        if response in validResponses:
            if response in validAResponses:
                self.response = AlternativeResponses.A.value
            elif response in validBResponses:
                self.response = AlternativeResponses.B.value
            elif response in validCResponses:
                self.response = AlternativeResponses.C.value
            return self.response
        else:
            return {"error": f"Por favor, responda com 'A', 'B' ou 'C'. Sua resposta foi: {message}"}