from enum import Enum
from .ResponseProcesser import YesMaybeOrNotResponses

class BeliefMatrix(Enum):
    NAO_CONTROLAVEL = "NAO_CONTROLAVEL"
    CONTROLAVEL = "CONTROLAVEL"
    PENUMBRA = "PENUMBRA"

def getBeliefByAnswer(answer: str) -> str:
    print("Answer: ", answer)
    if answer == YesMaybeOrNotResponses.YES.value:
        return BeliefMatrix.CONTROLAVEL.value
    elif answer == YesMaybeOrNotResponses.MAYBE.value:
        return BeliefMatrix.PENUMBRA.value
    elif answer == YesMaybeOrNotResponses.NOT.value:
        return BeliefMatrix.NAO_CONTROLAVEL.value