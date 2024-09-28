from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from ..crud import Elicitation as crudElicitation
from ..schemas import Elicitation as schemaElicitation
from ..db import getDBSession
from .EndpointsURL import (GET_ALL_FOCAL_QUESTIONS, GET_FOCAL_QUESTION)
from ..chatbot.ExtractFocalQuestionEntities import EntityExtractor

router = APIRouter()

@router.get(GET_ALL_FOCAL_QUESTIONS, response_model=List[schemaElicitation.Elicitation])
def getAllFocalQuestions(skip: int = 0, limit: int = 10, db: Session = Depends(getDBSession)):
    try:
        elicitations = crudElicitation.getElicitations(db, skip=skip, limit=limit)
        return elicitations
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@router.get(GET_FOCAL_QUESTION, response_model=schemaElicitation.ElicitationStatus)
def getFocalQuestion(focalQuestion: str, db: Session = Depends(getDBSession)):
    if not focalQuestion:
        raise HTTPException(status_code=404, detail="param 'focalQuestion' not received")
    try:
        elicitation = crudElicitation.getElicitationByFocalQuestion(db, focalQuestion)
        
        entities = EntityExtractor().extractEntities(focalQuestion=focalQuestion)
        print(entities)
        
        if not elicitation:
            # TODO - Criar lógica para criar agente, conceito e dominio quando não existir a QF ainda   
            elicitation = schemaElicitation.ElicitationStatus(focal_question=focalQuestion, agent=entities['AGENT'], concept=entities['CONCEPT'], domain=entities['DOMAIN'], id=None, isRegistered=False)
        else:
            elicitation.isRegistered = True
        return elicitation
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
