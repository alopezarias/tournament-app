from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.team import TeamCreate, TeamOut, TeamUpdate
from app.services.team_service import get_team, get_teams, create_team, update_team, delete_team
from app.db.session import get_db
from app.deps import get_current_player

router = APIRouter()

# GET ALL público
@router.get("/", response_model=list[TeamOut])
def read_teams(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_teams(db, skip, limit)

# Endpoints protegidos
@router.post("/", response_model=TeamOut)
def create_new_team(team: TeamCreate, db: Session = Depends(get_db), current_player = Depends(get_current_player)):
    # Se podría verificar que el jugador actual no tenga ya un equipo creado.
    return create_team(db, team)

@router.get("/{team_id}", response_model=TeamOut)
def read_team(team_id: int, db: Session = Depends(get_db), current_player = Depends(get_current_player)):
    db_team = get_team(db, team_id)
    if not db_team:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Equipo no encontrado")
    return db_team

@router.put("/{team_id}", response_model=TeamOut)
def update_existing_team(team_id: int, team: TeamUpdate, db: Session = Depends(get_db), current_player = Depends(get_current_player)):
    db_team = update_team(db, team_id, team)
    if not db_team:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Equipo no encontrado")
    return db_team

@router.delete("/{team_id}", response_model=TeamOut)
def delete_existing_team(team_id: int, db: Session = Depends(get_db), current_player = Depends(get_current_player)):
    db_team = delete_team(db, team_id)
    if not db_team:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Equipo no encontrado")
    return db_team
