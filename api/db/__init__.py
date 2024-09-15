from .Engine import DatabaseEngineManager
from .Session import getDBSession
from .Base import DatabaseBase

Engine = DatabaseEngineManager().getEngine()
Base = DatabaseBase.getBaseForDBModel()

__all__ = ["Engine", "getDBSession", "Base"]
