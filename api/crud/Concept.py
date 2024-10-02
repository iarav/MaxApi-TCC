from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from ..models.Concept import Concept
from ..schemas.Concept import ConceptCreate

def getConceptByMCEAndName(db: Session, mce_id: int, name: str):
    try:
        return db.query(Concept).filter(Concept.mce_id == mce_id, Concept.name == name).first()
    except SQLAlchemyError as e:
        return {"error": f"Error retrieving concept: {e}"}
    except Exception as e:
        return {"error": f"Unexpected error: {e}"}

def createConcept(db: Session, concept: ConceptCreate):
    try:
        dbConcept = Concept(
            name=concept.name,
            behavioral_belief=concept.behavioral_belief,
            normative_belief=concept.normative_belief,
            mce_id=concept.mce_id
        )
        db.add(dbConcept)
        db.commit()
        db.refresh(dbConcept)
        return dbConcept
    except SQLAlchemyError as e:
        db.rollback()
        return {"error": f"Error creating concept: {e}"}
    except Exception as e:
        db.rollback()
        return {"error": f"Unexpected error: {e}"}
    
def editConcept(db: Session, concept: ConceptCreate):
    try:
        dbConcept = db.query(Concept).filter(Concept.id == concept.id).first()
        if dbConcept:
            dbConcept.name = concept.name
            dbConcept.behavioral_belief = concept.behavioral_belief
            dbConcept.normative_belief = concept.normative_belief
            dbConcept.mce_id = concept.mce_id
            db.commit()
            db.refresh(dbConcept)
            return dbConcept
        else:
            return {"error": "Concept not found"}
    except SQLAlchemyError as e:
        db.rollback()
        return {"error": f"Error editing concept: {e}"}
    except Exception as e:
        db.rollback()
        return {"error": f"Unexpected error: {e}"}