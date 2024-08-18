from sqlalchemy.orm import Session
from ..models.elicitation import Elicitation
from ..schemas.elicitation import ElicitationCreate

def getElicitations(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Elicitation).offset(skip).limit(limit).all()

def getElicitationByFocalQuestion(db: Session, focalQuestion: str):
    return db.query(Elicitation).filter(Elicitation.focal_question == focalQuestion).first()

def createElicitation(db: Session, elicitation: ElicitationCreate):
    db_elicitation = Elicitation(
        focal_question=elicitation.focal_question,
        agent=elicitation.agent,
        concept=elicitation.concept,
        domain=elicitation.domain
    )
    db.add(db_elicitation)
    db.commit()
    db.refresh(db_elicitation)
    return db_elicitation
