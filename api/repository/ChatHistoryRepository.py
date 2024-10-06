from sqlalchemy.orm import Session
from ..crud import ChatHistory as crudChatHistory
from ..schemas import ChatHistory as schemaChatHistory
from ..schemas import MCE as schemaMCE
from typing import List
from ..helper.ErrorHandler import handleError

class ChatHistoryRepository:
    @staticmethod
    def addMessageToHistory(db: Session, message: str, sender: str, step: str, mce_id: int) -> None:
        chatHistoryCreate = schemaChatHistory.ChatHistoryCreate(
            message=message,
            sender=sender,
            step=step,
            mce_id=mce_id
        )
        response = crudChatHistory.addMessageToHistory(db, chatHistory=chatHistoryCreate)
        handleError(response)
    
    @staticmethod
    def getChatHistory(mce: schemaMCE.MCE, db: Session) -> List[schemaChatHistory.ChatHistory]:
        chatHistory = crudChatHistory.getMessageHistoryByMCE(db, mce_id=mce.id)
        handleError(chatHistory)
        return chatHistory
    
    def getLastStepByCurrentStep(db: Session, mce_id: int, currentStep: str):
        return crudChatHistory.getLastStepByCurrentStep(db, mce_id, currentStep)