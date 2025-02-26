# backend/app/schemas/tournament_bracket.py
from datetime import datetime
from pydantic import BaseModel

class TournamentBracketBase(BaseModel):
    phase: str
    match_id: int | None = None
    team_a_id: int
    team_b_id: int
    winner_team_id: int | None = None
    scheduled_date: datetime | None = None

class TournamentBracketCreate(TournamentBracketBase):
    pass

class TournamentBracketUpdate(BaseModel):
    phase: str | None = None
    match_id: int | None = None
    team_a_id: int | None = None
    team_b_id: int | None = None
    winner_team_id: int | None = None
    scheduled_date: datetime | None = None

class TournamentBracketOut(TournamentBracketBase):
    id: int

    class Config:
        orm_mode = True
