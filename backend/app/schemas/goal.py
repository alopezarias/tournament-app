from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class GoalBase(BaseModel):
    match_id: int
    player_id: Optional[int] = None
    sent_at: Optional[datetime] = None

class GoalCreate(GoalBase):
    pass

class GoalOut(GoalBase):
    id: int

    class Config:
        orm_mode = True
