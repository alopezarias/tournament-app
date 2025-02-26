# backend/app/schemas/tournament_standings.py
from pydantic import BaseModel

class TournamentStandingsOut(BaseModel):
    team_id: int
    wins: int
    draws: int
    losses: int
    goals_for: int
    goals_against: int
    points: int
    updated_at: str

    class Config:
        orm_mode = True
