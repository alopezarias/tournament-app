from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.match import MatchCreate, MatchOut, MatchUpdate
from app.services.match_service import get_match, get_matches, create_match, update_match, delete_match
from app.db.session import get_db
from app.deps import get_current_player

router = APIRouter()

# GET ALL se deja público
@router.get("/", response_model=list[MatchOut])
def read_matches(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_matches(db, skip, limit)

# Endpoints protegidos
@router.post("/", response_model=MatchOut)
def create_new_match(match: MatchCreate, db: Session = Depends(get_db), current_player = Depends(get_current_player)):
    return create_match(db, match)

@router.get("/{match_id}", response_model=MatchOut)
def read_match(match_id: int, db: Session = Depends(get_db), current_player = Depends(get_current_player)):
    db_match = get_match(db, match_id)
    if not db_match:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Partido no encontrado")
    return db_match

@router.put("/{match_id}", response_model=MatchOut)
def update_existing_match(match_id: int, match: MatchUpdate, db: Session = Depends(get_db), current_player = Depends(get_current_player)):
    db_match = update_match(db, match_id, match)
    if not db_match:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Partido no encontrado")
    return db_match

@router.delete("/{match_id}", response_model=MatchOut)
def delete_existing_match(match_id: int, db: Session = Depends(get_db), current_player = Depends(get_current_player)):
    db_match = delete_match(db, match_id)
    if not db_match:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Partido no encontrado")
    return db_match
