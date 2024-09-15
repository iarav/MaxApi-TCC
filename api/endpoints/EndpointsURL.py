GET_ALL_FOCAL_QUESTIONS = "/getAllFocalQuestions"
GET_FOCAL_QUESTION = "/getFocalQuestion"
# def GET_FOCAL_QUESTION(focalQuestion):
#     return f"/getFocalQuestion/{focalQuestion}"
def SIGN_IN(code):
    return f"/signIn/{code}"
def USER_INPUT(code, userInput):
    return f"/userInput/{code}/{userInput}"
CREATE_CHAT = "/createChat"

__all__ = [
    "GET_ALL_FOCAL_QUESTIONS",
    "GET_FOCAL_QUESTION",
    "SIGN_IN",
    "USER_INPUT",
    "CREATE_CHAT"
]