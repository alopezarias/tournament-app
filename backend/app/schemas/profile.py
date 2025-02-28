from pydantic import BaseModel
from app.schemas.player import PlayerOut

class ProfileOut(BaseModel):
    player: PlayerOut
    goals_scored: int
    matches_played: int
    tournament_position: int

    class Config:
        orm_mode = True
