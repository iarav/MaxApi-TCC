
from enum import Enum

class Steps(Enum):
    STEP_UNKNOWN = "STEP_UNKNOWN" # Unknown step
    STEP_ONE = "STEP_ONE" # Greeting and explaining focal question
    STEP_TWO = "STEP_TWO" # Making belief matrix positioning
    STEP_THREE_P1 = "STEP_THREE_P1" # Determine behavioral or normative belief
    STEP_THREE_P2 = "STEP_THREE_P2" # Determine behavioral or normative belief
    STEP_FOUR = "STEP_FOUR" # Define the second concept
    STEP_FIVE = "STEP_FIVE" # Define the relation_verb and relation_weight of the concept
    STEP_FIVE_P1 = "STEP_FIVE_P1" # Question about what to do next
    STEP_SIX = "STEP_SIX" # Define the relation of a concept to another one
    STEP_SEVEN = "STEP_SEVEN" # Define the relation direction of the relation defined on the previous step
    STEP_EIGHT = "STEP_EIGHT" # Add a new concept to the elicitation
    STEP_NINE = "STEP_NINE" # Add a new relation to the elicitation - first concept
    STEP_NINE_P2 = "STEP_NINE_P2" # Add a new relation to the elicitation - second concept
    STEP_CONDITION_TWO = "STEP_CONDITION_TWO" # Breakpoint for defining the next step
    STEP_CONDITION_ONE = "STEP_CONDITION_ONE" # Breakpoint for defining the next step
    STEP_END = "STEP_END" # End of the elicitation
    INCONCLUSIVE = "INCONCLUSIVE" # Inconclusive previous or next step

def getNextStep(step):
    if step == Steps.STEP_ONE.value:
        return Steps.STEP_TWO.value
    elif step == Steps.STEP_TWO.value:
        return Steps.STEP_THREE_P1.value
    elif step == Steps.STEP_THREE_P1.value:
        return Steps.STEP_THREE_P2.value
    elif step == Steps.STEP_THREE_P2.value:
        return Steps.STEP_CONDITION_ONE.value
    elif step == Steps.STEP_FOUR.value:
        return Steps.STEP_TWO.value
    elif step == Steps.STEP_FIVE.value:
        return Steps.STEP_FIVE_P1.value
    elif step == Steps.STEP_FIVE_P1.value:
        return Steps.STEP_CONDITION_TWO.value
    elif step == Steps.STEP_SIX.value:
        return Steps.STEP_SEVEN.value
    elif step == Steps.STEP_SEVEN.value:
        return Steps.STEP_FIVE.value
    elif step == Steps.STEP_EIGHT.value:
        return Steps.STEP_TWO.value
    elif step == Steps.STEP_NINE.value:
        return Steps.STEP_NINE_P2.value
    elif step == Steps.STEP_NINE_P2.value:
        return Steps.STEP_FIVE.value
    else:
        return None