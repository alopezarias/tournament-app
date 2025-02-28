from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.db.base_class import Base

class Invitation(Base):
    __tablename__ = "invitations"

    id = Column(Integer, primary_key=True, index=True)
    team_id = Column(Integer, ForeignKey("teams.id", ondelete="CASCADE"), nullable=False)
    inviter_id = Column(Integer, ForeignKey("players.id", ondelete="CASCADE"), nullable=False)
    invitee_id = Column(Integer, ForeignKey("players.id", ondelete="CASCADE"), nullable=False)
    status = Column(String(20), nullable=False, default='pending')  # pending, accepted, rejected
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
