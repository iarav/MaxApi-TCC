from sqlalchemy.orm import sessionmaker, Session
from contextlib import contextmanager
from .engine import DatabaseEngineManager

class DatabaseSession:
    def __init__(self):
        engine = DatabaseEngineManager()
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine.getEngine())

    @contextmanager
    def getDatabase(self):
        db = self.SessionLocal()
        try:
            yield db
        finally:
            db.close()

session_factory = DatabaseSession()

def getDBSession() -> Session:
    with session_factory.getDatabase() as db:
        return db