from pydantic import BaseModel
from typing import Optional

class PlayerBase(BaseModel):
    team_id: Optional[int] = None
    username: str
    name: str
    image: Optional[str] = None
    notifications_enabled: bool = True

class PlayerCreate(PlayerBase):
    pass

class PlayerUpdate(BaseModel):
    team_id: Optional[int] = None
    username: Optional[str] = None
    name: Optional[str] = None
    image: Optional[str] = None
    notifications_enabled: Optional[bool] = None

class PlayerOut(PlayerBase):
    id: int

    class Config:
        orm_mode = True
