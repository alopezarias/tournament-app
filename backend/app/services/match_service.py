from sqlalchemy.orm import Session
from app.models.match import Match
from app.schemas.match import MatchCreate, MatchUpdate

def get_match(db: Session, match_id: int):
    return db.query(Match).filter(Match.id == match_id).first()

def get_matches(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Match).offset(skip).limit(limit).all()

def create_match(db: Session, match: MatchCreate):
    db_match = Match(**match.dict())
    db.add(db_match)
    db.commit()
    db.refresh(db_match)
    return db_match

def update_match(db: Session, match_id: int, match_update: MatchUpdate):
    db_match = get_match(db, match_id)
    if not db_match:
        return None
    for key, value in match_update.dict(exclude_unset=True).items():
        setattr(db_match, key, value)
    db.commit()
    db.refresh(db_match)
    return db_match

def delete_match(db: Session, match_id: int):
    db_match = get_match(db, match_id)
    if not db_match:
        return None
    db.delete(db_match)
    db.commit()
    return db_match
