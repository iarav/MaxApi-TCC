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
