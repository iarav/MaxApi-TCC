from enum import Enum

class BeliefMatrix(Enum):
    NAO_CONTROLAVEL = "NAO_CONTROLAVEL"
    CONTROLAVEL = "CONTROLAVEL"
    PENUMBRA = "PENUMBRA"

def getBeliefByAnswer(answer: str) -> str:
    if answer == "sim" or answer == "s":
        return BeliefMatrix.CONTROLAVEL.value
    elif answer == "talvez":
        return BeliefMatrix.PENUMBRA.value
    elif answer == "nao" or answer == "n" or answer == "não":
        return BeliefMatrix.NAO_CONTROLAVEL.value