from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

load_dotenv()

class _DatabaseConfig:
    def __init__(self):
        self.url = os.getenv("DATABASE_URL", "")

class DatabaseEngineManager:
    def __init__(self):
        config = _DatabaseConfig()
        self.engine = create_engine(config.url)

    def getEngine(self):
        return self.engine