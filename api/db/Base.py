from sqlalchemy.ext.declarative import declarative_base

class DatabaseBase:
    @staticmethod
    def getBaseForDBModel():
        return declarative_base()
