from sqlalchemy.orm import Session
from app.models.tournament_standings import TournamentStandings

def get_standings(db: Session):
    return db.query(TournamentStandings).all()
