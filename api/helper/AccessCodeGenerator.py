from sqlalchemy.orm import Session
import random
import string
from ..crud import MCE as crudBase

class AccessCodeGenerator:
    @staticmethod
    def generateAccessCode(db: Session) -> str:
        access_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        while crudBase.getMCEByAccessCode(db, access_code=access_code):
            access_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        return access_code