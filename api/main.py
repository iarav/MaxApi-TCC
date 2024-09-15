from fastapi import FastAPI
from .db import Engine, Base
from .endpoints import FocalQuestions, Chat

Base.metadata.create_all(bind=Engine)

app = FastAPI()

app.include_router(FocalQuestions.router, prefix="/api/focalQuestion", tags=["focalQuestion"])
app.include_router(Chat.router, prefix="/api/chat", tags=["chat"])
