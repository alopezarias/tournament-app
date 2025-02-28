from pydantic import BaseModel
from typing import Optional

class TeamBase(BaseModel):
    name: str
    image: Optional[str] = None

class TeamCreate(TeamBase):
    pass

class TeamUpdate(BaseModel):
    name: Optional[str] = None
    image: Optional[str] = None

class TeamOut(TeamBase):
    id: int

    class Config:
        orm_mode = True
