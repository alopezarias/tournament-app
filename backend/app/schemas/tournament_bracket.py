from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class TournamentBracketBase(BaseModel):
    phase: str
    match_id: Optional[int] = None
    team_a_id: int
    team_b_id: int
    winner_team_id: Optional[int] = None
    scheduled_date: Optional[datetime] = None

class TournamentBracketCreate(TournamentBracketBase):
    pass

class TournamentBracketUpdate(BaseModel):
    phase: Optional[str] = None
    match_id: Optional[int] = None
    team_a_id: Optional[int] = None
    team_b_id: Optional[int] = None
    winner_team_id: Optional[int] = None
    scheduled_date: Optional[datetime] = None

class TournamentBracketOut(TournamentBracketBase):
    id: int

    class Config:
        orm_mode = True
