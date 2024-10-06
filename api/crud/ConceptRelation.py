from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from ..models.ConceptRelation import ConceptRelation
from ..schemas.ConceptRelation import ConceptRelationCreate

def getConceptRelationByConceptIds(db: Session, concept1_id: int = None, concept2_id: int = None):
    try:
        if concept2_id and concept1_id:
            return db.query(ConceptRelation).filter(ConceptRelation.concept1_id == concept1_id, ConceptRelation.concept2_id == concept2_id).first()
        elif concept1_id:
            return db.query(ConceptRelation).filter(ConceptRelation.concept1_id == concept1_id).order_by(ConceptRelation.concept1_id).first()
        elif concept2_id:
            return db.query(ConceptRelation).filter(ConceptRelation.concept2_id == concept2_id).order_by(ConceptRelation.concept2_id).first()
        else:
            return None
    except SQLAlchemyError as e:
        return {"error": f"Error retrieving concept relation: {e}"}
    except Exception as e:
        return {"error": f"Unexpected error: {e}"}

def createConceptRelation(db: Session, conceptRelation: ConceptRelationCreate):
    try:
        dbConceptRelation = ConceptRelation(
            concept1_id=conceptRelation.concept1_id,
            concept2_id=conceptRelation.concept2_id,
            relation_verb=conceptRelation.relation_verb,
            relation_weight=conceptRelation.relation_weight
        )
        db.add(dbConceptRelation)
        db.commit()
        db.refresh(dbConceptRelation)
        return dbConceptRelation
    except SQLAlchemyError as e:
        db.rollback()
        return {"error": f"Error creating concept: {e}"}
    except Exception as e:
        db.rollback()
        return {"error": f"Unexpected error: {e}"}
    
def editConceptRelation(db: Session, conceptRelation: ConceptRelationCreate):
    try:
        dbConceptRelation = db.query(ConceptRelation).filter(ConceptRelation.concept1_id == conceptRelation.concept1_id, ConceptRelation.concept2_id == conceptRelation.concept2_id).first()
        if dbConceptRelation:
            dbConceptRelation.relation_verb = conceptRelation.relation_verb
            dbConceptRelation.relation_weight = conceptRelation.relation_weight
            db.commit()
            db.refresh(dbConceptRelation)
            return dbConceptRelation
        else:
            return {"error": "Concept Relation not found to edit"}
    except SQLAlchemyError as e:
        db.rollback()
        return {"error": f"Error editing concept: {e}"}
    except Exception as e:
        db.rollback()
        return {"error": f"Unexpected error: {e}"}