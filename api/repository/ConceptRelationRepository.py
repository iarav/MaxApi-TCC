from sqlalchemy.orm import Session
from ..crud import ConceptRelation as crudConceptRelation
from ..schemas import ConceptRelation as schemaConceptRelation

class ConceptRelationRepository:
    @staticmethod
    def createIfNotExists(db: Session, conceptRelation: schemaConceptRelation.ConceptRelationCreate) -> schemaConceptRelation.ConceptRelation:
        dbConceptRelation = crudConceptRelation.getConceptRelationByConceptIds(db, concept1_id=conceptRelation.concept1_id, concept2_id=conceptRelation.concept2_id)
        if not dbConceptRelation:
            dbConceptRelation = crudConceptRelation.createConceptRelation(db, conceptRelation=conceptRelation)
        return dbConceptRelation