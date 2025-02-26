# backend/app/schemas/register.py
from pydantic import BaseModel, EmailStr

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    team_id: int
    username: str
    name: str
    image: str = None
