from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..crud import Agent as crud_agent
from ..crud import Elicitation as crud_elicitation
from ..crud import MCE as crud_base
from ..schemas import Agent as schema_agent
from ..schemas import Elicitation as schema_elicitation
from ..schemas import MCE as schema_mce
from datetime import datetime
from ..db import getDBSession
import random
import string
from EndpointsURL import (CREATE_CHAT, SIGN_IN, USER_INPUT)

router = APIRouter()

@router.post(CREATE_CHAT, response_model=schema_mce.MCE)
def create_chat(
    focal_question: schema_elicitation.ElicitationCreate,
    agent: schema_agent.AgentCreate,
    db: Session = Depends(getDBSession)
):
    db_agent = crud_agent.getAgentByEmail(db, email=agent.email)
    if not db_agent:
        db_agent = crud_agent.createAgent(db, agent=agent)
    
    db_elicitation = crud_elicitation.create_elicitation(db, elicitation=focal_question)
    
    access_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    # TODO - verificar se código existe e se existir, gerar outro
    mce = schema_mce.MCECreate(
        access_code=access_code,
        creation_date=datetime.utcnow(),
        agent_id=db_agent.id,
        elicitation_id=db_elicitation.id
    )
    
    db_mce = crud_base.create_mce(db, mce=mce)
    
    return db_mce

@router.get(SIGN_IN("{acess_code}"))
def sign_in(access_code: str, db: Session = Depends(getDBSession)):
    mce = crud_base.get_mce_by_access_code(db, access_code=access_code)
    if not mce:
        raise HTTPException(status_code=404, detail="Access code not found")
    return {"message": "Success", "access_code": access_code}

@router.get(USER_INPUT("{access_code}", "{user_input}"))
def process_user_input(access_code: str, user_input: str, db: Session = Depends(getDBSession)):
    mce = crud_base.get_mce_by_access_code(db, access_code=access_code)
    if not mce:
        raise HTTPException(status_code=404, detail="Access code not found")
    
    # TODO - Aqui você processaria o input do usuário com um chatbot
    chatbot_response = f"Resposta do chatbot para o input: {user_input}"
    
    return {"message": "Success", "response": chatbot_response}
