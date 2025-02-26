# backend/app/main.py
from fastapi import FastAPI
from app.controllers.auth_controller import router as auth_router
from app.controllers.team_controller import router as team_router
from app.controllers.player_controller import router as player_router
from app.controllers.match_controller import router as match_router
from app.controllers.goal_controller import router as goal_router
from app.controllers.tournament_standings_controller import router as standings_router
from app.controllers.tournament_bracket_controller import router as bracket_router

app = FastAPI(title="Torneo Futbolín API", version="1.0")

app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(team_router, prefix="/teams", tags=["teams"])
app.include_router(player_router, prefix="/players", tags=["players"])
app.include_router(match_router, prefix="/matches", tags=["matches"])
app.include_router(goal_router, prefix="/goals", tags=["goals"])
app.include_router(standings_router, prefix="/standings", tags=["standings"])
app.include_router(bracket_router, prefix="/brackets", tags=["brackets"])

@app.get("/")
def root():
    return {"message": "Bienvenido a la API del Torneo Futbolín"}
