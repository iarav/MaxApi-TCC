from sqlalchemy.orm import Session
from fastapi import HTTPException
from ..crud import Elicitation as crudElicitation
from ..schemas import Elicitation as schemaElicitation

class ElicitationRepository:
    @staticmethod
    def createIfNotExists(db: Session, focalQuestion: schemaElicitation.ElicitationCreate) -> schemaElicitation.Elicitation:
        dbElicitation = crudElicitation.getElicitationByFocalQuestion(db, focalQuestion.focal_question)
        if not dbElicitation:
            dbElicitation = crudElicitation.createElicitation(db, elicitation=focalQuestion)
            if not dbElicitation:
                raise HTTPException(status_code=400, detail="The params agent, concept, and domain must be provided in the body, inside the focal question")
        return dbElicitation