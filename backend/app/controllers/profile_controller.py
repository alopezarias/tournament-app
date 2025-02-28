from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.profile import ProfileOut
from app.services.profile_service import get_profile
from app.db.session import get_db
from app.deps import get_current_player

router = APIRouter()

@router.get("/", response_model=ProfileOut)
def get_profile_info(db: Session = Depends(get_db), current_player = Depends(get_current_player)):
    profile = get_profile(db, current_player.user_id)
    if not profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Perfil no encontrado")
    return profile
