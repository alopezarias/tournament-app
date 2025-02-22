from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.player import PlayerCreate, PlayerOut, PlayerUpdate
from app.services import player_service
from app.db.session import get_db

router = APIRouter()

@router.get("/", response_model=list[PlayerOut])
def read_players(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return player_service.get_players(db, skip=skip, limit=limit)

@router.post("/", response_model=PlayerOut)
def create_new_player(player: PlayerCreate, db: Session = Depends(get_db)):
    return player_service.create_player(db, player)

@router.get("/{player_id}", response_model=PlayerOut)
def read_player(player_id: int, db: Session = Depends(get_db)):
    db_player = player_service.get_player(db, player_id)
    if not db_player:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Player not found")
    return db_player

@router.put("/{player_id}", response_model=PlayerOut)
def update_existing_player(player_id: int, player: PlayerUpdate, db: Session = Depends(get_db)):
    db_player = player_service.update_player(db, player_id, player)
    if not db_player:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Player not found")
    return db_player

@router.delete("/{player_id}", response_model=PlayerOut)
def delete_existing_player(player_id: int, db: Session = Depends(get_db)):
    db_player = player_service.delete_player(db, player_id)
    if not db_player:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Player not found")
    return db_player
