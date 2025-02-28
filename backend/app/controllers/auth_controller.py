from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.schemas.register import RegisterRequest
from app.schemas.token import Token
from app.services.auth_service import create_user_and_player, authenticate_user, generate_tokens, verify_token
from app.db.session import get_db

router = APIRouter()

class LoginRequest(BaseModel):
    email: str
    password: str

@router.post("/register", response_model=Token)
def register(reg_req: RegisterRequest, db: Session = Depends(get_db)):
    try:
        # Crea el usuario y el jugador asociado; team_id puede ser None inicialmente.
        user, player = create_user_and_player(db, user_data=reg_req, player_data=reg_req)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    access_token, refresh_token = generate_tokens(user)
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}

@router.post("/login", response_model=Token)
def login(login_req: LoginRequest, db: Session = Depends(get_db)):
    user = authenticate_user(db, login_req.email, login_req.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales incorrectas")
    access_token, refresh_token = generate_tokens(user)
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}

@router.post("/refresh", response_model=Token)
def refresh_token(refresh_token: str, db: Session = Depends(get_db)):
    payload = verify_token(refresh_token)
    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token de refresco inválido")
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token mal formado")
    from app.models.user import User  # Importación local para evitar ciclos
    user = db.query(User).filter(User.id == int(user_id)).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuario no encontrado")
    access_token, new_refresh_token = generate_tokens(user)
    return {"access_token": access_token, "refresh_token": new_refresh_token, "token_type": "bearer"}
