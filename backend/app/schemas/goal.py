# backend/app/schemas/goal.py
from pydantic import BaseModel

class GoalBase(BaseModel):
    match_id: int
    player_id: int | None = None

class GoalCreate(GoalBase):
    pass

class GoalOut(GoalBase):
    id: int

    class Config:
        orm_mode = True
