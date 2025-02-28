from sqlalchemy.orm import Session
from app.models.tournament_bracket import TournamentBracket
from app.schemas.tournament_bracket import TournamentBracketCreate, TournamentBracketUpdate

def get_bracket(db: Session, bracket_id: int):
    return db.query(TournamentBracket).filter(TournamentBracket.id == bracket_id).first()

def get_brackets(db: Session, skip: int = 0, limit: int = 100):
    return db.query(TournamentBracket).offset(skip).limit(limit).all()

def create_bracket(db: Session, bracket: TournamentBracketCreate):
    db_bracket = TournamentBracket(**bracket.dict())
    db.add(db_bracket)
    db.commit()
    db.refresh(db_bracket)
    return db_bracket

def update_bracket(db: Session, bracket_id: int, bracket_update: TournamentBracketUpdate):
    db_bracket = get_bracket(db, bracket_id)
    if not db_bracket:
        return None
    for key, value in bracket_update.dict(exclude_unset=True).items():
        setattr(db_bracket, key, value)
    db.commit()
    db.refresh(db_bracket)
    return db_bracket

def delete_bracket(db: Session, bracket_id: int):
    db_bracket = get_bracket(db, bracket_id)
    if not db_bracket:
        return None
    db.delete(db_bracket)
    db.commit()
    return db_bracket
