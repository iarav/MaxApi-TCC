from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..crud import agent as crud_agent
from ..crud import elicitation as crud_elicitation
from ..crud import mce as crud_base
from ..schemas import agent as schema_agent
from ..schemas import elicitation as schema_elicitation
from ..schemas import mce as schema_mce
from datetime import datetime
from ..db import getDBSession
import random
import string

router = APIRouter()

@router.post("/createChat", response_model=schema_mce.MCE)
def create_chat(
    focal_question: schema_elicitation.ElicitationCreate,
    agent: schema_agent.AgentCreate,
    db: Session = Depends(getDBSession)
):
    db_agent = crud_agent.get_agent_by_email(db, email=agent.email)
    if not db_agent:
        db_agent = crud_agent.create_agent(db, agent=agent)
    
    db_elicitation = crud_elicitation.create_elicitation(db, elicitation=focal_question)
    
    access_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    mce = schema_mce.MCECreate(
        access_code=access_code,
        creation_date=datetime.utcnow(),
        agent_id=db_agent.id,
        elicitation_id=db_elicitation.id
    )
    
    db_mce = crud_base.create_mce(db, mce=mce)
    
    return db_mce

@router.get("/signIn/{access_code}")
def sign_in(access_code: str, db: Session = Depends(getDBSession)):
    mce = crud_base.get_mce_by_access_code(db, access_code=access_code)
    if not mce:
        raise HTTPException(status_code=404, detail="Access code not found")
    return {"message": "Success", "access_code": access_code}

@router.get("/getMCE/{access_code}", response_model=schema_mce.MCE)
def get_mce(access_code: str, db: Session = Depends(getDBSession)):
    mce = crud_base.get_mce_by_access_code(db, access_code=access_code)
    if not mce:
        raise HTTPException(status_code=404, detail="MCE not found")
    return mce

@router.get("/sendInput/{access_code}")
def send_input(access_code: str, user_input: str, db: Session = Depends(getDBSession)):
    mce = crud_base.get_mce_by_access_code(db, access_code=access_code)
    if not mce:
        raise HTTPException(status_code=404, detail="Access code not found")
    
    # Aqui você processaria o input do usuário com um chatbot
    chatbot_response = f"Resposta do chatbot para o input: {user_input}"
    
    return {"message": "Success", "response": chatbot_response}
