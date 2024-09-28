from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from ..models.MCE import MCE
from ..schemas.MCE import MCECreate

def createMCE(db: Session, mce: MCECreate):
    try:
        dbMCE = MCE(
            creation_date = mce.creation_date,
            update_date = mce.update_date,
            access_code = mce.access_code,
            agent_id = mce.agent_id,
            elicitation_id = mce.elicitation_id
        )
        db.add(dbMCE)
        db.commit()
        db.refresh(dbMCE)
        return dbMCE
    except SQLAlchemyError as e:
        db.rollback()
        print(f"Error creating MCE: {e}")
        return None

def getMCEByAccessCode(db: Session, access_code: str):
    try:
        return db.query(MCE).filter(MCE.access_code == access_code).first()
    except SQLAlchemyError as e:
        print(f"Error retrieving MCE by access code: {e}")
        return None
