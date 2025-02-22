from pydantic import BaseModel

class PlayerBase(BaseModel):
    team_id: int
    name: str
    image: str = None

class PlayerCreate(PlayerBase):
    pass

class PlayerUpdate(BaseModel):
    team_id: int | None = None
    name: str | None = None
    image: str | None = None

class PlayerOut(PlayerBase):
    id: int

    class Config:
        orm_mode = True
