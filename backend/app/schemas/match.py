# backend/app/schemas/match.py
from datetime import datetime
from pydantic import BaseModel

class MatchBase(BaseModel):
    team_a_id: int
    team_b_id: int
    score_team_a: int = 0
    score_team_b: int = 0
    match_date: datetime | None = None

class MatchCreate(MatchBase):
    pass

class MatchUpdate(BaseModel):
    team_a_id: int | None = None
    team_b_id: int | None = None
    score_team_a: int | None = None
    score_team_b: int | None = None
    match_date: datetime | None = None

class MatchOut(MatchBase):
    id: int

    class Config:
        orm_mode = True
