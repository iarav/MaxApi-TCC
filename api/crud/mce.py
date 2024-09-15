from sqlalchemy.orm import Session
from ..models.MCE import MCE
from ..schemas.MCE import MCECreate

def create_mce(db: Session, mce: MCECreate):
    db_mce = MCE(
        creation_date = mce.creation_date,
        access_code = mce.access_code
    )
    db.add(mce)
    db.commit()
    db.refresh(mce)
    return db_mce

def get_mce_by_access_code(db: Session, access_code: str):
    return db.query(MCE).filter(MCE.access_code == access_code).first()
