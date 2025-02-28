from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.tournament_bracket import TournamentBracketCreate, TournamentBracketOut, TournamentBracketUpdate
from app.services.tournament_bracket_service import get_bracket, get_brackets, create_bracket, update_bracket, delete_bracket
from app.db.session import get_db

router = APIRouter()

@router.get("/", response_model=list[TournamentBracketOut])
def read_brackets(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_brackets(db, skip, limit)

@router.post("/", response_model=TournamentBracketOut)
def create_new_bracket(bracket: TournamentBracketCreate, db: Session = Depends(get_db)):
    return create_bracket(db, bracket)

@router.get("/{bracket_id}", response_model=TournamentBracketOut)
def read_bracket(bracket_id: int, db: Session = Depends(get_db)):
    bracket = get_bracket(db, bracket_id)
    if not bracket:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bracket no encontrado")
    return bracket

@router.put("/{bracket_id}", response_model=TournamentBracketOut)
def update_existing_bracket(bracket_id: int, bracket: TournamentBracketUpdate, db: Session = Depends(get_db)):
    db_bracket = update_bracket(db, bracket_id, bracket)
    if not db_bracket:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bracket no encontrado")
    return db_bracket

@router.delete("/{bracket_id}", response_model=TournamentBracketOut)
def delete_existing_bracket(bracket_id: int, db: Session = Depends(get_db)):
    db_bracket = delete_bracket(db, bracket_id)
    if not db_bracket:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bracket no encontrado")
    return db_bracket
