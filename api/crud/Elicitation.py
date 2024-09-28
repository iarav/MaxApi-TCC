from sqlalchemy.orm import Session
from ..models.Elicitation import Elicitation
from ..schemas.Elicitation import ElicitationCreate

def getElicitations(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Elicitation).offset(skip).limit(limit).all()

def getElicitationByFocalQuestion(db: Session, focalQuestion: str):
    return db.query(Elicitation).filter(Elicitation.focal_question == focalQuestion).first()

def createElicitation(db: Session, elicitation: ElicitationCreate):
    print(elicitation)
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
