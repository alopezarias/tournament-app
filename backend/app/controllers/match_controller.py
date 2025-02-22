from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.match import MatchCreate, MatchOut, MatchUpdate
from app.services import match_service
from app.db.session import get_db

router = APIRouter()

@router.get("/", response_model=list[MatchOut])
def read_matches(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return match_service.get_matches(db, skip=skip, limit=limit)

@router.post("/", response_model=MatchOut)
def create_new_match(match: MatchCreate, db: Session = Depends(get_db)):
    return match_service.create_match(db, match)

@router.get("/{match_id}", response_model=MatchOut)
def read_match(match_id: int, db: Session = Depends(get_db)):
    db_match = match_service.get_match(db, match_id)
    if not db_match:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Match not found")
    return db_match

@router.put("/{match_id}", response_model=MatchOut)
def update_existing_match(match_id: int, match: MatchUpdate, db: Session = Depends(get_db)):
    db_match = match_service.update_match(db, match_id, match)
    if not db_match:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Match not found")
    return db_match

@router.delete("/{match_id}", response_model=MatchOut)
def delete_existing_match(match_id: int, db: Session = Depends(get_db)):
    db_match = match_service.delete_match(db, match_id)
    if not db_match:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Match not found")
    return db_match
