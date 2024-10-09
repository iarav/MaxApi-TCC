from sqlalchemy.orm import Session
from ..crud import ConceptRelation as crudConceptRelation
from ..schemas import ConceptRelation as schemaConceptRelation
from ..helper.ErrorHandler import handleError

class ConceptRelationRepository:
    @staticmethod
    def createIfNotExists(db: Session, conceptRelation: schemaConceptRelation.ConceptRelationCreate) -> schemaConceptRelation.ConceptRelation:
        dbConceptRelation = crudConceptRelation.getConceptRelationByConceptIds(db, concept1_id=conceptRelation.concept1_id, concept2_id=conceptRelation.concept2_id)
        if not dbConceptRelation:
            dbConceptRelation = crudConceptRelation.createConceptRelation(db, conceptRelation=conceptRelation)
        return dbConceptRelation
    
    def getCurrentConceptRelationAndConceptsByMCE(db: Session, mceId: int) -> schemaConceptRelation.ConceptRelationWithConcepts:
        dbConceptRelationJoinConcept = crudConceptRelation.getMostRecentConceptRelationByMCE(db, mce_id=mceId)
        handleError(dbConceptRelationJoinConcept)
        if not dbConceptRelationJoinConcept:
            return None
        conceptRelation, concept1, concept2 = dbConceptRelationJoinConcept
        conceptRelationWithConcepts = schemaConceptRelation.ConceptRelationWithConcepts(
            concept1_id=conceptRelation.concept1_id,
            concept2_id=conceptRelation.concept2_id,
            relation_weight=conceptRelation.relation_weight,
            concept1_name=concept1.name,
            concept2_name=concept2.name,
            concept1_behavioral_belief=concept1.behavioral_belief,
            concept1_normative_belief=concept1.normative_belief,
            concept2_behavioral_belief=concept2.behavioral_belief,
            concept2_normative_belief=concept2.normative_belief,
            mce_id=concept1.mce_id
        )
        return conceptRelationWithConcepts
    
    def addRelationWeightToConceptRelation(db: Session, conceptRelation: schemaConceptRelation.ConceptRelationCreate) -> schemaConceptRelation.ConceptRelation:
        dbConceptRelation = crudConceptRelation.editConceptRelation(db, conceptRelation=conceptRelation)
        return dbConceptRelation
    
    def getConceptRelationByConceptIds(db: Session, concept1_id: int, concept2_id: int) -> schemaConceptRelation.ConceptRelation:
        dbConceptRelation = crudConceptRelation.getConceptRelationByConceptIds(db, concept1_id=concept1_id, concept2_id=concept2_id)
        return dbConceptRelation