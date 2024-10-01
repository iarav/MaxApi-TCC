
from enum import Enum

class Steps(Enum):
    STEP_ONE = "STEP_ONE"
    STEP_TWO = "STEP_TWO"
    STEP_THREE_P1 = "STEP_THREE_P1"
    STEP_THREE_P2 = "STEP_THREE_P2"
    STEP_FOUR = "STEP_FOUR"
    STEP_FIVE = "STEP_FIVE"
    STEP_SIX = "STEP_SIX"
    STEP_SEVEN = "STEP_SEVEN"
    STEP_EIGHT = "STEP_EIGHT"
    STEP_NINE = "STEP_NINE"
    STEP_TEN = "STEP_TEN"

def getNextStep(step):
    if step == Steps.STEP_ONE.value:
        return Steps.STEP_TWO.value
    elif step == Steps.STEP_TWO.value:
        return Steps.STEP_THREE_P1.value
    elif step == Steps.STEP_THREE_P1.value:
        return Steps.STEP_THREE_P2.value
    elif step == Steps.STEP_THREE_P2.value:
        return Steps.STEP_FOUR.value
    elif step == Steps.STEP_FOUR.value:
        return Steps.STEP_FIVE.value
    elif step == Steps.STEP_FIVE.value:
        return Steps.STEP_SIX.value
    elif step == Steps.STEP_SIX.value:
        return Steps.STEP_SEVEN.value
    elif step == Steps.STEP_SEVEN.value:
        return Steps.STEP_EIGHT.value
    elif step == Steps.STEP_EIGHT.value:
        return Steps.STEP_NINE.value
    elif step == Steps.STEP_NINE.value:
        return Steps.STEP_TEN.value
    else:
        return None
    
def getPreviousStep(step):
    if step == Steps.STEP_TWO.value:
        return Steps.STEP_ONE.value
    elif step == Steps.STEP_THREE_P1.value:
        return Steps.STEP_TWO.value
    elif step == Steps.STEP_THREE_P2.value:
        return Steps.STEP_THREE_P1.value
    elif step == Steps.STEP_FOUR.value:
        return Steps.STEP_THREE_P2.value
    elif step == Steps.STEP_FIVE.value:
        return Steps.STEP_FOUR.value
    elif step == Steps.STEP_SIX.value:
        return Steps.STEP_FIVE.value
    elif step == Steps.STEP_SEVEN.value:
        return Steps.STEP_SIX.value
    elif step == Steps.STEP_EIGHT.value:
        return Steps.STEP_SEVEN.value
    elif step == Steps.STEP_NINE.value:
        return Steps.STEP_EIGHT.value
    elif step == Steps.STEP_TEN.value:
        return Steps.STEP_NINE.value
    else:
        return None