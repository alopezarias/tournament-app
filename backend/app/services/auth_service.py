from sqlalchemy.orm import Session
from app.models.user import User
from app.models.player import Player
from app.schemas.user import UserCreate
from app.schemas.player import PlayerCreate
from passlib.context import CryptContext
from app.core.security import create_access_token, create_refresh_token, verify_token

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def create_user_and_player(db: Session, user_data: UserCreate, player_data: PlayerCreate):
    # Verifica que el email y el username sean únicos
    if get_user_by_email(db, user_data.email):
        raise ValueError("El email ya está registrado.")
    if db.query(Player).filter(Player.username == player_data.username).first():
        raise ValueError("El username ya está en uso.")

    # Crear el usuario (para autenticación)
    hashed_password = pwd_context.hash(user_data.password)
    db_user = User(email=user_data.email, password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    # Crear el jugador asociado (team_id se puede dejar en None)
    db_player = Player(
        user_id=db_user.id,
        team_id=player_data.team_id,  # Inicialmente, puede ser None
        username=player_data.username,
        name=player_data.name,
        image=player_data.image,
        notifications_enabled=True  # Por defecto, se habilitan
    )
    db.add(db_player)
    db.commit()
    db.refresh(db_player)

    return db_user, db_player


def authenticate_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)
    if not user:
        return None
    if not pwd_context.verify(password, user.password):
        return None
    return user


def generate_tokens(user: User):
    access_token = create_access_token(data={"sub": str(user.id)})
    refresh_token = create_refresh_token(data={"sub": str(user.id)})
    return access_token, refresh_token
