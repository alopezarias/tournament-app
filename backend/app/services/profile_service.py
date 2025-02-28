def get_profile(db, user_id: int):
    from app.models.player import Player
    from app.models.goal import Goal
    from app.models.match import Match
    from app.models.tournament_standings import TournamentStandings

    # Obtener el jugador asociado al usuario
    player = db.query(Player).filter(Player.user_id == user_id).first()
    if not player:
        return None
    # Calcular estadísticas
    goals_scored = db.query(Goal).filter(Goal.player_id == player.id).count()
    if player.team_id:
        matches_played = db.query(Match).filter(
            (Match.team_a_id == player.team_id) | (Match.team_b_id == player.team_id)
        ).count()
        standings = db.query(TournamentStandings).filter(TournamentStandings.team_id == player.team_id).first()
        tournament_position = standings.points if standings else 0
    else:
        matches_played = 0
        tournament_position = 0
    return {
        "player": player,
        "goals_scored": goals_scored,
        "matches_played": matches_played,
        "tournament_position": tournament_position
    }
