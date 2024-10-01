from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from ..models.ChatHistory import ChatHistory
from ..schemas.ChatHistory import ChatHistoryCreate
from datetime import datetime, timezone

def addMessageToHistory(db: Session, chatHistory: ChatHistoryCreate):
    try:
        new_message = ChatHistory(
            message=chatHistory.message,
            sender=chatHistory.sender,
            step=chatHistory.step,
            mce_id=chatHistory.mce_id,
            timestamp=datetime.now(timezone.utc)
        )
        db.add(new_message)
        db.commit()
        db.refresh(new_message)
        return new_message
    except SQLAlchemyError as e:
        db.rollback()
        return {"error": f"Error adding message to history: {e}"}
    except Exception as e:
        db.rollback()
        return {"error": f"Unexpected error: {e}"}

def getMessageHistoryByMCE(db: Session, mce_id: int):
    try:
        return db.query(ChatHistory).filter(ChatHistory.mce_id == mce_id).order_by(ChatHistory.timestamp).all()
    except SQLAlchemyError as e:
        return {"error": f"Error retrieving message history: {e}"}
    except Exception as e:
        return {"error": f"Unexpected error: {e}"}
    
def getLastStepMessagesByMCE(db: Session, mce_id: int):
    try:
        mostRecentStep = db.query(ChatHistory).filter(ChatHistory.mce_id == mce_id).order_by(ChatHistory.timestamp.desc()).first()
        if mostRecentStep:
            mostRecentStep = mostRecentStep.step
            return db.query(ChatHistory).filter(ChatHistory.mce_id == mce_id, ChatHistory.step == mostRecentStep).order_by(ChatHistory.timestamp).all()
        else:
            return []
    except SQLAlchemyError as e:
        return {"error": f"Error retrieving last step messages: {e}"}
    except Exception as e:
        return {"error": f"Unexpected error: {e}"}

def getMessagesByStepAndSender(db: Session, mce_id: int, step: str, sender: str):
    try:
        return db.query(ChatHistory).filter(ChatHistory.mce_id == mce_id, ChatHistory.step == step, ChatHistory.sender == sender).order_by(ChatHistory.timestamp).all()
    except SQLAlchemyError as e:
        return {"error": f"Error retrieving messages by step and sender: {e}"}
    except Exception as e:
        return {"error": f"Unexpected error: {e}"}