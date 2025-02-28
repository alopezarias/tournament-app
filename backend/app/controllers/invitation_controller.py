from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.invitation import InvitationCreate, InvitationOut, InvitationRespond
from app.services.invitation_service import create_invitation, respond_invitation, get_invitations_for_player
from app.db.session import get_db
from app.deps import get_current_player

router = APIRouter()

@router.post("/", response_model=InvitationOut)
def send_invitation(invitation: InvitationCreate, db: Session = Depends(get_db), current_player = Depends(get_current_player)):
    try:
        return create_invitation(db, invitation)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.post("/{invitation_id}/respond", response_model=InvitationOut)
def respond_to_invitation(invitation_id: int, response: InvitationRespond, db: Session = Depends(get_db), current_player = Depends(get_current_player)):
    try:
        return respond_invitation(db, invitation_id, response)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/player/{player_id}", response_model=list[InvitationOut])
def get_invitations(player_id: int, db: Session = Depends(get_db), current_player = Depends(get_current_player)):
    # Aquí se puede opcionalmente verificar que player_id == current_player.id para privacidad.
    if int(player_id) != current_player.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No puedes ver invitaciones de otro jugador")
    return get_invitations_for_player(db, player_id)
