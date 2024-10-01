from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from ..models.Elicitation import Elicitation
from ..schemas.Elicitation import ElicitationCreate

def getElicitations(db: Session, skip: int = 0, limit: int = 10):
    try:
        return db.query(Elicitation).offset(skip).limit(limit).all()
    except SQLAlchemyError as e:
        return {"error": str(e)}

def getElicitationByFocalQuestion(db: Session, focalQuestion: str):
    try:
        return db.query(Elicitation).filter(Elicitation.focal_question == focalQuestion).first()
    except SQLAlchemyError as e:
        return {"error": str(e)}
    
def getElicitationById(db: Session, elicitation_id: int):
    try:
        return db.query(Elicitation).filter(Elicitation.id == elicitation_id).first()
    except SQLAlchemyError as e:
        return {"error": str(e)}

def createElicitation(db: Session, elicitation: ElicitationCreate):
    try:
        if(elicitation.agent == None or elicitation.concept == None or elicitation.domain == None):
            return None
        
        dbElicitation = Elicitation(
            focal_question=elicitation.focal_question,
            agent=elicitation.agent,
            concept=elicitation.concept,
            domain=elicitation.domain
        )
        db.add(dbElicitation)
        db.commit()
        db.refresh(dbElicitation)
        return dbElicitation
    except SQLAlchemyError as e:
        db.rollback()
        return {"error": str(e)}
