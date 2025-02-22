from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.tournament_standings import TournamentStandingsOut
from app.services import tournament_standings_service
from app.db.session import get_db

router = APIRouter()

@router.get("/", response_model=list[TournamentStandingsOut])
def read_standings(db: Session = Depends(get_db)):
    return tournament_standings_service.get_standings(db)
