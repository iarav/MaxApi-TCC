from .engine import DatabaseEngineManager
from .session import getDBSession
from .base import DatabaseBase

engine = DatabaseEngineManager().getEngine()
Base = DatabaseBase.getBaseForDBModel()

__all__ = ["engine", "getDBSession", "Base"]
