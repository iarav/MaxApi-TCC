from sqlalchemy.orm import Session
from fastapi import HTTPException
from datetime import datetime
from ..crud import MCE as crudBase
from ..schemas import MCE as schemaMCE

class MCERepository:
    @staticmethod
    def createMCE(db: Session, access_code: str, agent_id: int, elicitation_id: int) -> schemaMCE.MCE:
        mce = schemaMCE.MCECreate(
            access_code=access_code,
            creation_date=datetime.now(),
            update_date=datetime.now(),
            agent_id=agent_id,
            elicitation_id=elicitation_id
        )
        return crudBase.createMCE(db, mce=mce)
    
    @staticmethod
    def getMCE(access_code: str, db: Session) -> schemaMCE.MCE:
        mce = crudBase.getMCEByAccessCode(db, access_code=access_code)
        if not mce:
            raise HTTPException(status_code=404, detail="Access code not found")
        return mce