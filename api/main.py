from fastapi import FastAPI
from .db import Engine, Base
from .endpoints import FocalQuestions, Chat
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=Engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(FocalQuestions.router, prefix="/api/focalQuestion", tags=["focalQuestion"])
app.include_router(Chat.router, prefix="/api/chat", tags=["chat"])
