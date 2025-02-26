# backend/app/models/tournament_bracket.py
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, CheckConstraint
from sqlalchemy.sql import func
from app.db.base_class import Base

class TournamentBracket(Base):
    __tablename__ = "tournament_bracket"

    id = Column(Integer, primary_key=True, index=True)
    phase = Column(String(50), nullable=False)  # Ej.: 'Octavos', 'Cuartos', 'Semifinal', 'Final'
    match_id = Column(Integer, ForeignKey("matches.id", ondelete="CASCADE"), nullable=True)
    team_a_id = Column(Integer, ForeignKey("teams.id", ondelete="CASCADE"), nullable=False)
    team_b_id = Column(Integer, ForeignKey("teams.id", ondelete="CASCADE"), nullable=False)
    winner_team_id = Column(Integer, ForeignKey("teams.id", ondelete="SET NULL"), nullable=True)
    scheduled_date = Column(DateTime)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    __table_args__ = (
        CheckConstraint('team_a_id <> team_b_id', name='different_teams_bracket'),
    )
