from sqlalchemy.orm import Session
from ..crud import Concept as crudConcept
from ..schemas import Concept as schemaConcept
from ..helper.ErrorHandler import handleError

class ConceptRepository:
    @staticmethod
    def createIfNotExists(db: Session, concept: schemaConcept.ConceptCreate) -> schemaConcept.Concept:
        dbConcept = crudConcept.getConceptByMCEAndName(db, mceId=concept.mce_id, name=concept.name)
        handleError(dbConcept)
        if not dbConcept:
            dbConcept = crudConcept.createConcept(db, concept=concept)
            handleError(dbConcept)
            return dbConcept
        else:
            return None
        
    @staticmethod
    def getConceptByName(db: Session, mceId: int, name: str) -> schemaConcept.Concept:
        dbConcept = crudConcept.getConceptByMCEAndName(db, mceId=mceId, name=name)
        handleError(dbConcept)
        return dbConcept