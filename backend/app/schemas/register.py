from pydantic import BaseModel, EmailStr
from typing import Optional

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    team_id: Optional[int] = None
    username: str
    name: str
    image: Optional[str] = None
