from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..schemas import Agent as schemaAgent
from ..schemas import Elicitation as schemaElicitation
from ..schemas import MCE as schemaMCE
from ..schemas import Chat as schemaChat
from ..db import getDBSession
from .EndpointsURL import (CREATE_CHAT, SIGN_IN, USER_INPUT, GET_ALL_CHAT_HISTORY)
from ..services.ChatService import generateChatbotResponseByUserInput, getAllChatHistory, signInAgent, createChatbot

router = APIRouter()

@router.post(CREATE_CHAT, response_model=schemaMCE.MCE)
def createChat(
    focalQuestion: schemaElicitation.ElicitationCreate,
    agent: schemaAgent.AgentCreate,
    db: Session = Depends(getDBSession)
):
    return createChatbot(focalQuestion, agent, db)

@router.get(SIGN_IN)
def signIn(access_code: str, db: Session = Depends(getDBSession)):
    return signInAgent(access_code, db)

@router.get(GET_ALL_CHAT_HISTORY)
def getChatHistory(access_code: str, db: Session = Depends(getDBSession)):
    return getAllChatHistory(access_code, db)

@router.post(USER_INPUT, response_model=dict)
def processUserInput(user_data: schemaChat.CreateUserInput, db: Session = Depends(getDBSession)):
    return generateChatbotResponseByUserInput(user_data, db)

def checkError(response):
    if isinstance(response, dict) and response.get("error"):
        raise HTTPException(status_code=500, detail=response.get("error"))