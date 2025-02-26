from pydantic import BaseModel

class TeamBase(BaseModel):
    name: str
    image: str = None

class TeamCreate(TeamBase):
    pass

class TeamUpdate(BaseModel):
    name: str | None = None
    image: str | None = None

class TeamOut(TeamBase):
    id: int

    class Config:
        orm_mode = True
