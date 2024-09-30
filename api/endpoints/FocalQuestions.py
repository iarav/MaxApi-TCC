from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from ..crud import Elicitation as crudElicitation
from ..schemas import Elicitation as schemaElicitation
from ..db import getDBSession
from .EndpointsURL import GET_ALL_FOCAL_QUESTIONS, GET_FOCAL_QUESTION
from ..chatbot.ExtractFocalQuestionEntities import EntityExtractor

router = APIRouter()

def _handleException(e: Exception, detail: str):
    if isinstance(e, SQLAlchemyError):
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Database error: {str(e)}")
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"{detail}: {str(e)}")

@router.get(GET_ALL_FOCAL_QUESTIONS, response_model=List[schemaElicitation.Elicitation])
def getAllFocalQuestions(skip: int = 0, limit: int = 10, db: Session = Depends(getDBSession)):
    try:
        elicitations = crudElicitation.getElicitations(db, skip=skip, limit=limit)
        return elicitations
    except Exception as e:
        _handleException(e, "Unexpected error")

@router.get(GET_FOCAL_QUESTION, response_model=schemaElicitation.ElicitationStatus)
def getFocalQuestion(focalQuestion: str, db: Session = Depends(getDBSession)):
    if not focalQuestion:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="param 'focalQuestion' not received")
    try:
        elicitation = crudElicitation.getElicitationByFocalQuestion(db, focalQuestion)
        
        if not elicitation:
            entities = EntityExtractor().extractEntities(focalQuestion=focalQuestion) 
            elicitation = schemaElicitation.ElicitationStatus(
                focal_question=focalQuestion, 
                agent=entities['AGENT'], 
                concept=entities['CONCEPT'], 
                domain=entities['DOMAIN'], 
                id=None, 
                isRegistered=False
            )
        else:
            elicitation.isRegistered = True
        return elicitation
    except Exception as e:
        _handleException(e, "Unexpected error")
