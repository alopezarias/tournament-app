# backend/app/controllers/tournament_standings_controller.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.tournament_standings import TournamentStandingsOut
from app.services.tournament_standings_service import get_standings
from app.db.session import get_db

router = APIRouter()

@router.get("/", response_model=list[TournamentStandingsOut])
def read_standings(db: Session = Depends(get_db)):
    standings = get_standings(db)
    for standing in standings:
        standing.updated_at = standing.updated_at.strftime("%Y-%m-%dT%H:%M:%S %p")
    return standings
