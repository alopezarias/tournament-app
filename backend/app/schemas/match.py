from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class MatchBase(BaseModel):
    team_a_id: int
    team_b_id: int
    score_team_a: int = 0
    score_team_b: int = 0
    match_date: Optional[datetime] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    status: Optional[str] = None
    duration: Optional[str] = None  # Cadena que representa el intervalo

class MatchCreate(MatchBase):
    pass

class MatchUpdate(BaseModel):
    team_a_id: Optional[int] = None
    team_b_id: Optional[int] = None
    score_team_a: Optional[int] = None
    score_team_b: Optional[int] = None
    match_date: Optional[datetime] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None

class MatchOut(MatchBase):
    id: int

    class Config:
        orm_mode = True
