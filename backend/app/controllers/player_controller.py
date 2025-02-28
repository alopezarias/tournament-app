from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.player import PlayerOut, PlayerUpdate
from app.services.player_service import get_player, get_players, update_player, delete_player
from app.db.session import get_db
from app.deps import get_current_player

router = APIRouter()

# GET ALL público: se devuelve solo información básica (usando el esquema PlayerOut que ya no incluye credenciales)
@router.get("/", response_model=list[PlayerOut])
def read_players(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_players(db, skip, limit)

# Endpoints protegidos:
@router.get("/me", response_model=PlayerOut)
def read_current_player(current_player = Depends(get_current_player)):
    # Devuelve la información del jugador actual (sin credenciales)
    return current_player

@router.get("/{player_id}", response_model=PlayerOut)
def read_player(player_id: int, db: Session = Depends(get_db), current_player = Depends(get_current_player)):
    # Opcional: permitir solo el propio jugador o datos públicos.
    db_player = get_player(db, player_id)
    if not db_player:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Jugador no encontrado")
    return db_player

@router.put("/{player_id}", response_model=PlayerOut)
def update_existing_player(player_id: int, player: PlayerUpdate, db: Session = Depends(get_db), current_player = Depends(get_current_player)):
    if current_player.id != player_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No puedes modificar otro jugador")
    db_player = update_player(db, player_id, player)
    if not db_player:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Jugador no encontrado")
    return db_player

@router.delete("/{player_id}", response_model=PlayerOut)
def delete_existing_player(player_id: int, db: Session = Depends(get_db), current_player = Depends(get_current_player)):
    if current_player.id != player_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No puedes eliminar otro jugador")
    db_player = delete_player(db, player_id)
    if not db_player:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Jugador no encontrado")
    return db_player

@router.put("/{player_id}/notifications", response_model=PlayerOut)
def update_notifications(player_id: int, enabled: bool, db: Session = Depends(get_db), current_player = Depends(get_current_player)):
    if current_player.id != player_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No puedes modificar otro jugador")
    update_data = {"notifications_enabled": enabled}
    db_player = update_player(db, player_id, update_data)
    if not db_player:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Jugador no encontrado")
    return db_player
