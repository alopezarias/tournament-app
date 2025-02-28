from sqlalchemy.orm import Session
from app.models.invitation import Invitation
from app.models.player import Player
from app.models.team import Team
from app.schemas.invitation import InvitationCreate

def create_invitation(db: Session, invitation_data: InvitationCreate):
    # Verificar que el jugador invitado no tenga ya un equipo
    invitee = db.query(Player).filter(Player.id == invitation_data.invitee_id).first()
    if not invitee:
        raise ValueError("Jugador invitado no encontrado.")
    if invitee.team_id is not None:
        raise ValueError("El jugador ya pertenece a un equipo.")
    db_invite = Invitation(**invitation_data.dict())
    db.add(db_invite)
    db.commit()
    db.refresh(db_invite)
    return db_invite

def respond_invitation(db: Session, invitation_id: int, response_data):
    invitation = db.query(Invitation).filter(Invitation.id == invitation_id).first()
    if not invitation:
        raise ValueError("Invitación no encontrada.")
    if invitation.status != 'pending':
        raise ValueError("La invitación ya ha sido respondida.")
    invitation.status = response_data.response  # 'accepted' o 'rejected'
    db.commit()
    db.refresh(invitation)
    if invitation.status == 'accepted':
        # Actualiza el team_id del jugador invitado y cierra el equipo
        invitee = db.query(Player).filter(Player.id == invitation.invitee_id).first()
        invitee.team_id = invitation.team_id
        team = db.query(Team).filter(Team.id == invitation.team_id).first()
        team.is_closed = True
        # Rechaza las invitaciones pendientes para ese equipo
        db.query(Invitation).filter(
            Invitation.team_id == invitation.team_id,
            Invitation.status == 'pending'
        ).update({"status": "rejected"})
        db.commit()
    return invitation

def get_invitations_for_player(db: Session, player_id: int):
    return db.query(Invitation).filter(Invitation.invitee_id == player_id, Invitation.status == 'pending').all()
