from fastapi import FastAPI
from .db import engine, Base
from .endpoints import focalquestions, chat

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(focalquestions.router, prefix="/api/focalquestions", tags=["focalquestions"])
app.include_router(chat.router, prefix="/api/chat", tags=["chat"])
