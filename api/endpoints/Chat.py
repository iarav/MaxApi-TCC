from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..crud import Agent as crudAgent
from ..crud import Elicitation as crudElicitation
from ..crud import MCE as crudBase
from ..crud import ChatHistory as crudChatHistory
from ..schemas import ChatHistory as schemaChatHistory
from ..schemas import Agent as schemaAgent
from ..schemas import Elicitation as schemaElicitation
from ..schemas import MCE as schemaMCE
from ..schemas import Chat as schemaChat
from datetime import datetime
from ..db import getDBSession
import random 
import string
from .EndpointsURL import (CREATE_CHAT, SIGN_IN, USER_INPUT, GET_ALL_CHAT_HISTORY)
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
        checkError(dbAgent)
        if not dbAgent:
            dbAgent = crudAgent.createAgent(db, agent=agent)
            checkError(dbAgent)
        
        dbElicitation = crudElicitation.getElicitationByFocalQuestion(db, focalQuestion=focalQuestion.focal_question)
        checkError(dbElicitation)
        if not dbElicitation:
            dbElicitation = crudElicitation.createElicitation(db, elicitation=focalQuestion)
            print(dbElicitation)
            if not dbElicitation:
                raise HTTPException(status_code=400, detail="the params agent, concept, and domain must be provided in the body, inside the focal question") 
        
        accessCode = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        while crudBase.getMCEByAccessCode(db, access_code=accessCode):
            checkError(mce)
            accessCode = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        mce = schemaMCE.MCECreate(
            access_code=accessCode,
            creation_date=datetime.now(),
            update_date=datetime.now(),
            agent_id=dbAgent.id,
            elicitation_id=dbElicitation.id
        )
        
        dbMCE = crudBase.createMCE(db, mce=mce)
        checkError(dbMCE)
        
        return dbMCE
    except HTTPException as e:
        raise e
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))

@router.get(SIGN_IN)
def sign_in(access_code: str, db: Session = Depends(getDBSession)):
    try:
        mce = crudBase.getMCEByAccessCode(db, access_code=access_code)
        checkError(mce)
        if not mce:
            raise HTTPException(status_code=401, detail="Unauthorized - invalid Access code")
        return {"message": "Success", "access_code": access_code}
    except HTTPException as e:
        raise e
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))

@router.get(GET_ALL_CHAT_HISTORY)
def get_chat_history(access_code: str, db: Session = Depends(getDBSession)):
    try:
        mce = crudBase.getMCEByAccessCode(db, access_code=access_code)
        checkError(mce)
        if not mce:
            raise HTTPException(status_code=404, detail="Access code not found")
        
        chatHistory = crudChatHistory.getMessageHistoryByMCE(db, mce_id=mce.id)
        checkError(chatHistory)
        return chatHistory
    except HTTPException as e:
        raise e
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))

@router.post(USER_INPUT, response_model=dict)
def process_user_input(user_data: schemaChat.CreateUserInput, db: Session = Depends(getDBSession)):
    try:
        mce = crudBase.getMCEByAccessCode(db, access_code=user_data.access_code)
        if not mce:
            raise HTTPException(status_code=404, detail="Access code not found")
        
        chatHistory = crudChatHistory.getMessageHistoryByMCE(db, mce_id=mce.id)
        checkError(chatHistory)
        print(chatHistory)

        chatbot_response = ""
        if user_data.user_input == "":
            chatbot_response = MaxResponses.greeting(mce.agent.name.capitalize())
        else:
            chatbot_response = f"Resposta do chatbot para o input: {user_data.user_input}"
        
        print(chatbot_response)
        if user_data.user_input != "":
            crudChatHistory.addMessageToHistory(db, chatHistory=schemaChatHistory.ChatHistoryCreate(
                message=user_data.user_input,
                sender="user",
                mce_id=mce.id
            ))
            checkError(message)
        if chatbot_response != "":
            message = crudChatHistory.addMessageToHistory(db, chatHistory=schemaChatHistory.ChatHistoryCreate(
                message=chatbot_response,
                sender="chatbot",
                mce_id=mce.id
            ))
            checkError(message)
        # TODO - Aqui você processaria o input do usuário com um chatbot
        return {"message": "Success", "response": chatbot_response}
    except HTTPException as e:
        raise e
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))

def checkError(response):
    if isinstance(response, dict) and response.get("error"):
        raise HTTPException(status_code=500, detail=response.get("error"))