from sqlalchemy.orm import Session
from app.models.player import Player
from app.schemas.player import PlayerCreate, PlayerUpdate

def get_player(db: Session, player_id: int):
    return db.query(Player).filter(Player.id == player_id).first()

def get_players(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Player).offset(skip).limit(limit).all()

def update_player(db: Session, player_id: int, player_update: PlayerUpdate):
    db_player = get_player(db, player_id)
    if not db_player:
        return None
    for key, value in player_update.dict(exclude_unset=True).items():
        setattr(db_player, key, value)
    db.commit()
    db.refresh(db_player)
    return db_player

def delete_player(db: Session, player_id: int):
    db_player = get_player(db, player_id)
    if not db_player:
        return None
    db.delete(db_player)
    db.commit()
    return db_player
