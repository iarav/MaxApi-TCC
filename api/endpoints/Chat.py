from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..crud import Agent as crudAgent
from ..crud import Elicitation as crudElicitation
from ..crud import MCE as crudBase
from ..schemas import Agent as schemaAgent
from ..schemas import Elicitation as schemaElicitation
from ..schemas import MCE as schemaMCE
from datetime import datetime
from ..db import getDBSession
import random 
import string
from .EndpointsURL import (CREATE_CHAT, SIGN_IN, USER_INPUT)
from ..chatbot.MaxResponses import MaxResponses

router = APIRouter()

@router.post(CREATE_CHAT, response_model=schemaMCE.MCE)
def createChat(
    focalQuestion: schemaElicitation.ElicitationCreate,
    agent: schemaAgent.AgentCreate,
    db: Session = Depends(getDBSession)
):
    try:
        dbAgent = crudAgent.getAgentByEmail(db, email=agent.email)
        if not dbAgent:
            dbAgent = crudAgent.createAgent(db, agent=agent)
        
        dbElicitation = crudElicitation.getElicitationByFocalQuestion(db, focalQuestion=focalQuestion.focal_question)
        if not dbElicitation:
            dbElicitation = crudElicitation.createElicitation(db, elicitation=focalQuestion)
            if not dbElicitation:
                raise HTTPException(status_code=400, detail="the params agent, concept, and domain must be provided in the body, inside the focal question") 
        
        accessCode = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        while crudBase.getMCEByAccessCode(db, access_code=accessCode):
            accessCode = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        mce = schemaMCE.MCECreate(
            access_code=accessCode,
            creation_date=datetime.now(),
            update_date=datetime.now(),
            agent_id=dbAgent.id,
            elicitation_id=dbElicitation.id
        )
        
        dbMCE = crudBase.createMCE(db, mce=mce)
        
        return dbMCE
    except HTTPException as e:
        raise e
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))

@router.get(SIGN_IN)
def sign_in(access_code: str, db: Session = Depends(getDBSession)):
    mce = crudBase.getMCEByAccessCode(db, access_code=access_code)
    if not mce:
        raise HTTPException(status_code=401, detail="Unauthorized - invalid Access code")
    return {"message": "Success", "access_code": access_code}

@router.get(USER_INPUT)
def process_user_input(access_code: str, user_input: str, db: Session = Depends(getDBSession)):
    mce = crudBase.getMCEByAccessCode(db, access_code=access_code)
    if not mce:
        raise HTTPException(status_code=404, detail="Access code not found")
    
    chatbot_response = ""
    if(user_input == ""):
        chatbot_response = MaxResponses.greeting(mce.agent.name.capitalize())
    else:
        chatbot_response = f"Resposta do chatbot para o input: {user_input}"
        
    # TODO - Aqui você processaria o input do usuário com um chatbot
    
    return {"message": "Success", "response": chatbot_response}
