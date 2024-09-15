from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from ..crud import Elicitation as crud_elicitation
from ..schemas import Elicitation as schemaElicitation
from ..db import getDBSession
from EndpointsURL import (GET_ALL_FOCAL_QUESTIONS, GET_FOCAL_QUESTION)

router = APIRouter()

@router.get(GET_ALL_FOCAL_QUESTIONS, response_model=List[schemaElicitation.Elicitation])
def read_elicitations(skip: int = 0, limit: int = 10, db: Session = Depends(getDBSession)):
    elicitations = crud_elicitation.getElicitations(db, skip=skip, limit=limit)
    return elicitations

@router.get(GET_FOCAL_QUESTION("{focalQuestion}"), response_model=schemaElicitation.Elicitation)
def read_focalquestion(focalQuestion: str, db: Session = Depends(getDBSession)):
    if not focalQuestion:
        raise HTTPException(status_code=404, detail="focalQuestion not received as param")
    elicitation = crud_elicitation.getElicitationByFocalQuestion(db, focalQuestion)
    if not elicitation:
        # TODO - Criar lógica para criar agente, conceito e dominio quando não existir a QF ainda
        raise HTTPException(status_code=404, detail="Elicitation not found")
    return elicitation
