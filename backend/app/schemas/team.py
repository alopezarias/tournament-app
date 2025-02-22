# backend/app/schemas/team.py
from pydantic import BaseModel

class TeamBase(BaseModel):
    name: str
    image: str = None

class TeamCreate(TeamBase):
    pass

class TeamOut(TeamBase):
    id: int

    class Config:
        orm_mode = True
