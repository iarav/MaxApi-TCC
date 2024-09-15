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

router = APIRouter()

@router.post(CREATE_CHAT, response_model=schemaMCE.MCE)
def create_chat(
    focal_question: schemaElicitation.ElicitationCreate,
    agent: schemaAgent.AgentCreate,
    db: Session = Depends(getDBSession)
):
    db_agent = crudAgent.getAgentByEmail(db, email=agent.email)
    if not db_agent:
        db_agent = crudAgent.createAgent(db, agent=agent)
    
    db_elicitation = crudElicitation.create_elicitation(db, elicitation=focal_question)
    
    access_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    # TODO - verificar se código existe e se existir, gerar outro
    mce = schemaMCE.MCECreate(
        access_code=access_code,
        creation_date=datetime.utcnow(),
        agent_id=db_agent.id,
        elicitation_id=db_elicitation.id
    )
    
    db_mce = crudBase.create_mce(db, mce=mce)
    
    return db_mce

@router.get(SIGN_IN("{acess_code}"))
def sign_in(access_code: str, db: Session = Depends(getDBSession)):
    mce = crudBase.get_mce_by_access_code(db, access_code=access_code)
    if not mce:
        raise HTTPException(status_code=404, detail="Access code not found")
    return {"message": "Success", "access_code": access_code}

@router.get(USER_INPUT("{access_code}", "{user_input}"))
def process_user_input(access_code: str, user_input: str, db: Session = Depends(getDBSession)):
    mce = crudBase.get_mce_by_access_code(db, access_code=access_code)
    if not mce:
        raise HTTPException(status_code=404, detail="Access code not found")
    
    # TODO - Aqui você processaria o input do usuário com um chatbot
    chatbot_response = f"Resposta do chatbot para o input: {user_input}"
    
    return {"message": "Success", "response": chatbot_response}
