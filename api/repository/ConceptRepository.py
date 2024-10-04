from sqlalchemy.orm import Session
from ..crud import Concept as crudConcept
from ..schemas import Concept as schemaConcept

class ConceptRepository:
    @staticmethod
    def createIfNotExists(db: Session, concept: schemaConcept.ConceptCreate) -> schemaConcept.Concept:
        dbConcept = crudConcept.getConceptByMCEAndName(db, mceId=concept.mce_id, name=concept.name)
        if not dbConcept:
            dbConcept = crudConcept.createConcept(db, concept=concept)
        return dbConcept